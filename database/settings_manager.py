# database/settings_manager.py

from sqlalchemy import create_engine, Column, Integer, String, select
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Setting(Base):
    __tablename__ = 'settings'

    id = Column(Integer, primary_key=True)
    key = Column(String, nullable=False, unique=True)
    value = Column(String, nullable=False)

class SettingsManager:
    def __init__(self, db_path='sqlite:///config/settings.db'):
        self.engine = create_engine(db_path, future=True)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine, future=True)

    def get_theme(self):
        return self.get_setting('theme') or 'light'

    def set_theme(self, theme):
        self.set_setting('theme', theme)

    def get_setting(self, key):
        with self.Session() as session:
            stmt = select(Setting).where(Setting.key == key)
            setting = session.execute(stmt).scalar_one_or_none()
            return setting.value if setting else None

    def set_setting(self, key, value):
        with self.Session() as session:
            stmt = select(Setting).where(Setting.key == key)
            setting = session.execute(stmt).scalar_one_or_none()
            if setting:
                setting.value = value
            else:
                setting = Setting(key=key, value=value)
                session.add(setting)
            session.commit()
