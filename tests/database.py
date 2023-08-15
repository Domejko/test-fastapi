from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings as set


SQLALCHEMY_DATABASE_URL = f'postgresql://{set.database_username}:{set.database_password}@{set.database_hostname}:{set.database_port}/{set.test_database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
