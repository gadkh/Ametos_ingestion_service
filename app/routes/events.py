from fastapi import APIRouter, Depends, status, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ..db.session_handler import get_session
from ..schemas.event import EventCreate, EventResponse
from ..services.event_service import save_event, get_filtered_events, validate_event

router = APIRouter()


@router.post("/events", status_code=status.HTTP_201_CREATED, response_model=EventCreate)
async def create_event(event: EventCreate, db: Session = Depends(get_session)):
    device_type = await validate_event(db=db, event=event)
    if not device_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid sensor")
    event.device_type = device_type
    db_event = await save_event(db=db, event=event)
    return db_event


@router.get("/events", response_model=List[EventResponse])
def get_events(
    db: Session = Depends(get_session),
    start_time: Optional[datetime] = Query(None, description="Filter events after this timestamp"),
    end_time: Optional[datetime] = Query(None, description="Filter events before this timestamp"),
    event_type: Optional[str] = Query(None, description="Filter events by event type"),
    device_type: Optional[str] = Query(None, description="Filter events by device type")
):
    events = get_filtered_events(db, start_time, end_time, event_type, device_type)
    return events

