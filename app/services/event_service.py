from sqlalchemy.orm import Session
from ..db.models.events import Event
from ..db.models.sensors import Sensor
from ..schemas.event import EventCreate, EventResponse
from ..workers.celery_worker import process_event
from typing import Optional, List
from datetime import datetime
import redis


redis_client = redis.StrictRedis(host="localhost", port=6379, db=0, decode_responses=True)
UNVALID_SENSORS_SET = "unvalid_sensors"


async def validate_event(db: Session, event: EventCreate):
    device_type = redis_client.get(event.device_id)

    if device_type:
        return device_type

    if redis_client.sismember(UNVALID_SENSORS_SET, event.device_id):
        return None

    sensor = db.query(Sensor).filter(Sensor.device_id == event.device_id).first()
    if sensor:
        redis_client.set(sensor.device_id, sensor.device_type)
        return device_type

    redis_client.sadd(UNVALID_SENSORS_SET, event.device_id)
    return None


async def save_event(db: Session, event: EventCreate):
    db_event = Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    process_event.delay(event.dict())
    return db_event


def get_filtered_events(
    db: Session,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    event_type: Optional[str] = None,
    device_type: Optional[str] = None
) -> List[EventResponse]:

    query = db.query(Event)

    if start_time:
        query = query.filter(Event.timestamp >= start_time)
    if end_time:
        query = query.filter(Event.timestamp <= end_time)
    if event_type:
        query = query.filter(Event.event_type == event_type)
    if device_type:
        query = query.filter(Event.device_type == device_type)

    return query.all()