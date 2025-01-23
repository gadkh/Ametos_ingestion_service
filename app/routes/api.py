from fastapi import APIRouter
from .events import router as events_router

router = APIRouter(prefix="/v1")

router.include_router(events_router)
