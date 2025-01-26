from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional
import base64


class EventCreate(BaseModel):
    device_id: str
    timestamp: datetime
    event_type: str
    device_type: Optional[str] = None
    user_id: Optional[str] = None
    speed_kmh: Optional[int] = None
    location: Optional[str] = None
    zone: Optional[str] = None
    confidence: Optional[float] = None
    photo_base64: Optional[str] = None


class EventResponse(BaseModel):
    id: int
    device_id: str
    timestamp: datetime
    event_type: str
    device_type: str

    class Config:
        from_attributes = True