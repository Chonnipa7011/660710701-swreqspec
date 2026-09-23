import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base


DATABASE_URL = os.getenv("DATABASE_URL")


def get_engine():
    """Create the configured MySQL engine; supports CON-TECH-01 without choosing a driver."""
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL must be configured for the MySQL deployment")
    return create_engine(DATABASE_URL, pool_pre_ping=True)


def create_schema() -> None:
    """Create booking tables on MySQL; supports CON-TECH-01 and DOM-PDPA-01."""
    Base.metadata.create_all(bind=get_engine())


def get_db():
    """Provide a database session for booking data access; supports CON-TECH-01."""
    session = sessionmaker(bind=get_engine(), autoflush=False, autocommit=False)()
    try:
        yield session
    finally:
        session.close()