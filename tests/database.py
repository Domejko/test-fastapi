from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from app.config import settings as set
from app.main import app
from app.database import get_db
from app import models



SQLALCHEMY_DATABASE_URL = f'postgresql://{set.database_username}:{set.database_password}@{set.database_hostname}:{set.database_port}/{set.test_database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def get_test_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = get_test_db
    yield TestClient(app)

    # session.execute(text("TRUNCATE users RESTART IDENTITY CASCADE"))
