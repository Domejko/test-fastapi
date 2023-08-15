import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings as set
from app.main import app
from app.database import get_db
from app import models, oauth2



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


@pytest.fixture
def create_test_user(client):
    response = client.post('/users', json={'email': 'test@gmail.com', 'password': 'password123'})
    response_2 = client.post('/users', json={'email': 'test1@gmail.com', 'password': 'password123'})

    new_user = response.json()
    new_user_2 = response_2.json()

    return new_user, new_user_2


@pytest.fixture
def token(create_test_user):
    return oauth2.create_access_token({'user_id': create_test_user[0]['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        'Authorization': f'Bearer {token}'
    }
    return client


@pytest.fixture
def create_test_post(session, create_test_user):
    posts = [{'title': 'test post', 'content': 'test content', 'published': True, 'user_id': create_test_user[0]['id']},
            {'title': 'test post 1', 'content': 'test content 1', 'published': True, 'user_id': create_test_user[1]['id']}]
    
    def create_post_model(post):
        return models.Post(**post)
    
    posts = map(create_post_model, posts)
    session.add_all(posts)
    session.commit()

