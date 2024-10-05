# database/history_manager.py

from sqlalchemy import create_engine, Column, Integer, String, DateTime, select
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

Base = declarative_base()

class History(Base):
    __tablename__ = 'history'

    id = Column(Integer, primary_key=True)
    device_name = Column(String, nullable=False)
    mac_address = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

class HistoryManager:
    def __init__(self, db_path='sqlite:///config/settings.db'):
        self.engine = create_engine(db_path, future=True)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine, future=True)

    def add_entry(self, device_name, mac_address):
        with self.Session() as session:
            entry = History(
                device_name=device_name,
                mac_address=mac_address
            )
            session.add(entry)
            session.commit()

    def get_history(self, limit=50):
        with self.Session() as session:
            stmt = select(History).order_by(History.timestamp.desc()).limit(limit)
            entries = session.execute(stmt).scalars().all()
            result = [{
                'device_name': entry.device_name,
                'mac_address': entry.mac_address,
                'timestamp': entry.timestamp
            } for entry in entries]
        return result
