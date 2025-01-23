from sqlalchemy.orm import Session
from ..db.models.events import Event
from ..schemas.event import EventCreate
# from app.celery_worker import process_event

def save_event(db: Session, event: EventCreate):
    db_event = Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    # process_event.delay(event.dict())
    return db_event
