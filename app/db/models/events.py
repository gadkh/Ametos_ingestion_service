from sqlalchemy import Column, String, Integer, TIMESTAMP, Float
from ..session_handler import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)
    event_type = Column(String, nullable=False)
    user_id = Column(String, nullable=True)
    speed_kmh = Column(Integer, nullable=True)
    location = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, server_default="now()")
    device_type = Column(String, nullable=False)
    zone = Column(String, nullable=True)
    confidence = Column(Float, nullable=True )
    photo_base64 = Column(String, nullable=True)
