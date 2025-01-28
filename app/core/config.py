import os
from dotenv import load_dotenv

running_in_docker = os.getenv("RUNNING_IN_DOCKER")
if not running_in_docker:
    load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/iot_db")
REDIS_URL = os.getenv("REDIS_URL", "redis://ingestion_redis:6379/0")
RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")
MOCK_DATA_FILE = os.getenv("MOKE_SENSOR_DATA", "sensors_data/moke.json")