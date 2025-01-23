from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class EventCreate(BaseModel):
    device_id: str
    timestamp: datetime
    event_type: str
    user_id: Optional[str] = None
    speed_kmh: Optional[int] = None
    location: Optional[str] = None
