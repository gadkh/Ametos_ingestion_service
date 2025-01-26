import json
from sqlalchemy.orm import Session
from app.db.models.sensors import Sensor
from .config import MOCK_DATA_FILE


def load_mock_data(db: Session):
    with open(MOCK_DATA_FILE, "r") as file:
        sensors = json.load(file)
    for sensor in sensors:
        new_sensor = Sensor(device_id=sensor["device_id"], device_type=sensor["device_type"])
        db.add(new_sensor)
    db.commit()
    print("Mock data loaded successfully.")


def delete_mock_data(db: Session):
    db.query(Sensor).delete()
    db.commit()
    print("Mock data deleted successfully.")
