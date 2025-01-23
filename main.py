from app.db.session_handler import Base, engine
from fastapi import FastAPI
from app.routes.api import router

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Ingestion service",
    debug=True,
    version="0.1"
)


@app.get("/")
def root():
    return {"Message": "Root worked"}


app.include_router(router)