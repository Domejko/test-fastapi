from pydantic_core import ValidationError
from jose import jwt
import pytest

from app import schemas, oauth2
from app.config import settings



@pytest.mark.parametrize('email, password', [
    ('test@gmail.com', 'password123'),
    ('testgmailcom', 'password')
])
def test_create_user(client, email, password):
    response = client.post('/users', json={'email': email, 'password': password})
    
    try:
        new_user = schemas.UserResponse(**response.json())
        assert response.status_code == 201
        assert new_user.email == email
    except:
        assert ValidationError   


def test_get_user(client, create_test_user):
    response = client.get('/users/1')
    user_info = schemas.UserResponse(**response.json())

    assert user_info.id == 1
    assert user_info.email == 'test@gmail.com'
    assert response.status_code == 200


@pytest.mark.parametrize('email, password', [
    ('test@gmail.com', 'password123'),
    ('test@gmail.com', 'password'),
    ('test@test.com', 'password'),
    (None, 'password1234'),
    ('test@gmail.com', None)
])
def test_user_login(client, email, password, create_test_user):
    response = client.post('/login', data={'username': email, 'password': password})

    try:
        token = schemas.Token(**response.json())
        payload = jwt.decode(token.access_token, settings.secret_key, algorithms=[settings.algorithm])
        id = payload.get('user_id')

        assert id == 1
        assert token.token_type == 'bearer'
        assert token.access_token == oauth2.create_access_token({'user_id': 1})
        assert response.status_code == 200
    except ValidationError:
        if email == None or password == None:
            assert response.status_code == 422
        else:
            assert response.status_code == 403

    

    