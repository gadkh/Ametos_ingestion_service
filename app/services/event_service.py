import base64

from sqlalchemy.orm import Session
from ..db.models.events import Event
from ..db.models.sensors import Sensor
from ..schemas.event import EventCreate, EventResponse
from ..workers.celery_worker import process_event
from typing import Optional, List
from datetime import datetime
from ..db.redis_client import redis_client

INVALID_SENSORS_SET = "invalid_sensors"


def validate_cache_sensor(device_id: str):
    device_type =  redis_client.get(device_id)
    if device_type:
        return device_type
    return None


def set_valid_cache_sensor(device_id, device_type):
    redis_client.set(device_id,device_type)


def set_invalid_cache_sensor(device_id):
    redis_client.sadd(INVALID_SENSORS_SET, device_id)


def invalidate_cache_sensor(device_id: str):
    device_type = redis_client.sismember(INVALID_SENSORS_SET, device_id)
    if device_type:
        return device_type
    return None


async def validate_db_sensor(db: Session, event: EventCreate):
    sensor = db.query(Sensor).filter(Sensor.device_id == event.device_id).first()
    if sensor:
        return sensor.device_type
    return None


async def validate_event(db: Session, event: EventCreate):
    print(f"event::: {event}")
    device_type = redis_client.get(event.device_id)
    if device_type is not None:
        return device_type

    if redis_client.sismember(INVALID_SENSORS_SET, event.device_id):
        return None

    sensor = db.query(Sensor).filter(Sensor.device_id == event.device_id).first()
    if sensor:
        redis_client.set(sensor.device_id, sensor.device_type)
        print(f"sensor.device_type: {sensor.device_type}")
        return sensor.device_type

    redis_client.sadd(INVALID_SENSORS_SET, event.device_id)
    return None


def encode_image_to_base64(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string


async def save_event(db: Session, event: EventCreate):
    if event.device_type == "security_camera":
        if event.zone == "Restricted Area":
            event.photo_base64 = encode_image_to_base64(f"assets/intrusion-detection-1-alert.jpg")
        else:
            event.photo_base64 = encode_image_to_base64(f"assets/intrusion-detection-2-no-alert.jpg")
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