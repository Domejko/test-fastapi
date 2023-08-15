from pydantic_core import ValidationError
import pytest

from app import schemas



def test_root(client):
    response = client.get('/')
    assert response.json().get('message') == 'Hello World ! Succefull deploy !'
    assert response.status_code == 200


def test_get_post(authorized_client, create_test_post):
    response = authorized_client.get('/posts')
    posts = schemas.PostBase(**response.json()[0]['Post'])
    
    assert posts.title == 'test post'
    assert posts.content == 'test content'
    assert response.status_code == 200


@pytest.mark.parametrize('id, response_code', [
    (1, 200),
    (3, 404)
])
def test_get_post_by_id(authorized_client, create_test_post, id, response_code):
    response = authorized_client.get(f'/posts/{id}')

    if id == 1:
        posts = schemas.PostOut(**response.json())

        assert posts.Post.title == 'test post'
        assert posts.Post.content == 'test content'
        assert posts.Post.user_id == id
        assert response.status_code == response_code
    else:
        assert response.status_code == response_code




@pytest.mark.parametrize('post_content, response_code', [
    ({'title': 'test post', 'content': 'test content', 'published': 'TRUE'}, 201),
    ({'title': None, 'content': 'test content', 'published': 'TRUE'}, 422),
    ({'title': 'test post', 'content': None, 'published': 'TRUE'}, 422),
])
def test_posting(authorized_client, post_content, response_code):
    post: schemas.PostCreate = post_content
    response = authorized_client.post('/posts', json=post)

    try:
        posts = schemas.PostOut(**response.json())

        assert posts.Post.title == 'test post'
        assert posts.Post.content == 'test content'
        assert posts.Post.user_id == 1
        assert response.status_code == response_code
    except ValidationError:
        assert response.status_code == response_code


@pytest.mark.parametrize('post_id, response_code', [
    (1, 204),
    (2, 403),
    (3, 404)
])
def test_delete_post(authorized_client, create_test_post, post_id, response_code):
    pass
    response = authorized_client.delete(f'posts/{post_id}')

    assert response.status_code == response_code


@pytest.mark.parametrize('post_content, id, response_code', [
    ({'title': 'updated post', 'content': 'updated content', 'published': 'TRUE'}, 1, 200),
    ({'title': None, 'content': 'updated test content', 'published': 'TRUE'}, 1, 422),
    ({'title': 'updated test post', 'content': None, 'published': 'TRUE'}, 1, 422),
    ({'title': 'updated test post', 'content': 'updated test content', 'published': 'TRUE'}, 2, 403),
    ({'title': 'updated test post', 'content': 'updated test content', 'published': 'TRUE'}, 3, 404),
])
def test_update_post(authorized_client, create_test_post, post_content, id, response_code):
    post: schemas.PostCreate = post_content
    response = authorized_client.put(f'/posts/{id}', json=post)

    try:
        posts = schemas.PostOut(**response.json())

        assert posts.Post.title == 'updated test post'
        assert posts.Post.content == 'updated test content'
        assert posts.Post.user_id == 1
        assert response.status_code == response_code
    except ValidationError:
        assert response.status_code == response_code