# database/device_manager.py

from sqlalchemy import create_engine, Column, Integer, String, select
from sqlalchemy.orm import declarative_base, sessionmaker
from utils.encryption import EncryptionManager

Base = declarative_base()

class Device(Base):
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    mac_address = Column(String, nullable=False)
    ip_address = Column(String)

class DeviceManager:
    def __init__(self, db_path='sqlite:///config/settings.db'):
        self.engine = create_engine(db_path, future=True)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine, future=True)

        self.encryption_manager = EncryptionManager()

    def add_device(self, name, mac_address, ip_address=None):
        encrypted_mac = self.encryption_manager.encrypt(mac_address)
        encrypted_ip = self.encryption_manager.encrypt(ip_address) if ip_address else None

        with self.Session() as session:
            # Vérification des doublons
            stmt = select(Device).where(Device.mac_address == encrypted_mac)
            existing_device = session.execute(stmt).scalar_one_or_none()
            if existing_device:
                return False  # Le périphérique existe déjà

            device = Device(
                name=name,
                mac_address=encrypted_mac,
                ip_address=encrypted_ip
            )
            session.add(device)
            session.commit()
        return True

    def get_all_devices(self):
        result = []
        with self.Session() as session:
            stmt = select(Device)
            devices = session.execute(stmt).scalars().all()
            for device in devices:
                result.append({
                    'id': device.id,
                    'name': device.name,
                    'mac_address': self.encryption_manager.decrypt(device.mac_address),
                    'ip_address': self.encryption_manager.decrypt(device.ip_address) if device.ip_address else None
                })
        return result
    
    def delete_device(self, device_id):
        with self.Session() as session:
            device = session.get(Device, device_id)
            if device:
                session.delete(device)
                session.commit()
                return True
            else:
                return False
            