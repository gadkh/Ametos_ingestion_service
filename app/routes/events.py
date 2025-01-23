from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db.session_handler import get_session
from ..schemas.event import EventCreate
from ..services.event_service import save_event

router = APIRouter()


@router.post("/events")
def create_event(event: EventCreate, db: Session = Depends(get_session)):
    save_event(db, event)
    return {"message": "Event saved successfully"}