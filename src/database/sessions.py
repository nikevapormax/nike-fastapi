from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config.settings.base import project_settings

SQLALCHEMY_DATABASE_URL = "".join(
    [
        "postgresql://",
        f"{project_settings.POSTGRES_USER}:{project_settings.POSTGRES_PASSWORD}@",
        f"{project_settings.POSTGRES_SERVER}:{project_settings.POSTGRES_PORT}/",
        f"{project_settings.POSTGRES_DB}",
    ]
)
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)
