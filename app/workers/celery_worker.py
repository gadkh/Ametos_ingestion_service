from celery import Celery
import os

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
REDIS_BACKEND = os.getenv("REDIS_URL", "redis://localhost:6379/0")


celery_app = Celery(
    "ingestion_service",
    broker=RABBITMQ_URL,
    backend=REDIS_BACKEND
)

celery_app.conf.task_routes = {
    'tasks.process_event': {'queue': 'Sensors'}
}


@celery_app.task(name="tasks.process_event")
def process_event(event_data):
    print(f"Processing event: {event_data}")
    return f"Processed event {event_data['device_id']}"




