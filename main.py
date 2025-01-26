from app.db.session_handler import Base, engine
from fastapi import FastAPI
from app.routes.api import router
from app.db.session_handler import get_session
from app.core.load_moke_data import load_mock_data, delete_mock_data

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Ingestion service",
    debug=True,
    version="0.1"
)


@app.on_event("startup")
async def startup_event():
    with next(get_session()) as db:
        load_mock_data(db)


@app.on_event("shutdown")
async def shutdown_event():
    with next(get_session()) as db:
        delete_mock_data(db)


@app.get("/")
def root():
    return {"Message": "Root worked"}


app.include_router(router)