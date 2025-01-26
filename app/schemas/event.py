from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class EventCreate(BaseModel):
    device_id: str
    timestamp: datetime
    event_type: str
    device_type: Optional[str] = None
    user_id: Optional[str] = None
    speed_kmh: Optional[int] = None
    location: Optional[str] = None


class EventResponse(BaseModel):
    id: int
    device_id: str
    timestamp: datetime
    event_type: str
    device_type: str

    class Config:
        # orm_mode = True
        from_attributes = True
