import pytest

from app import models


@pytest.fixture()
def create_test_vote(create_test_post, session, create_test_user):
    new_vote = models.Vote(post_id= 2, user_id=1)
    session.add(new_vote)
    session.commit()


@pytest.mark.parametrize('post_id, post_dir, response_status', [
    (2, 1, 201),
    (2, 0, 404),
    (3, 1, 404),
])
def test_upvote_novote_nopost(authorized_client, create_test_post,  post_id, post_dir, response_status):
    response = authorized_client.post('/vote', json={'post_id': post_id, 'post_dir': post_dir})

    assert response.status_code == response_status


@pytest.mark.parametrize('post_id, post_dir, response_status', [
    (2, 1, 409),
    (2, 0, 201)
])
def test_downvote_double_vote(authorized_client, create_test_post, create_test_vote, post_id, post_dir, response_status):
    response = authorized_client.post('/vote', json={'post_id': post_id, 'post_dir': post_dir})

    assert response.status_code == response_status


def test_unauthorized_user(client, create_test_post):
    response = client.post('/vote', json={'post_id': 2, 'post_dir': 1})

    assert response.status_code == 401
    