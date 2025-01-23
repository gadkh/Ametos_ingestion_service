from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..core.config import DATABASE_URL

# DB_URL = "sqlite:///./app/db.sql"
DB_URL = DATABASE_URL

engine = create_engine(url=DB_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False)
Base = declarative_base()


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
