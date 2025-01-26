from sqlalchemy import Column, String
from ..session_handler import Base

class Sensor(Base):
    __tablename__ = "sensors"

    device_id = Column(String, primary_key=True, index=True)
    device_type = Column(String, nullable=False)
