import pytest
from app.schemas.event import EventCreate
from app.db.models.events import Event
from app.db.session_handler import SessionLocal
from datetime import datetime
import redis

# Mock Redis client
mock_redis_client = redis.StrictRedis(decode_responses=True)


@pytest.fixture
def sample_event():
    return EventCreate(
        device_id="AA:BB:CC:DD:EE:FF",
        timestamp=datetime.utcnow(),
        event_type="access_attempt",
        device_type="access_controller",
        user_id="admin0011",
        speed_kmh=None,
        location=None,
        zone=None,
        confidence=None,
        photo_base64=None
    )


@pytest.fixture
def db_session():
    db = SessionLocal()
    yield db
    db.close()


def test_event_validation(sample_event):
    assert sample_event.device_id == "AA:BB:CC:DD:EE:FF"
    assert sample_event.event_type == "access_attempt"


def test_redis_caching(sample_event):
    device_id = sample_event.device_id
    mock_redis_client.set(device_id, sample_event.device_type)

    cached_type = mock_redis_client.get(device_id)
    assert cached_type == "access_controller"


def test_event_persistence(db_session, sample_event):
    new_event = Event(**sample_event.dict())
    db_session.add(new_event)
    db_session.commit()

    saved_event = db_session.query(Event).filter_by(device_id="AA:BB:CC:DD:EE:FF").first()
    assert saved_event is not None
    assert saved_event.device_type == "access_controller"
