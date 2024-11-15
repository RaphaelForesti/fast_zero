from http import HTTPStatus
from random import randint

from fast_zero.schemas import UserPublic, UserSchema


def test_create_user(client, temp_user):
    response = client.post(
        '/users/',
        json={
            'username': temp_user.username,
            'password': temp_user.password,
            'email': temp_user.email,
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': temp_user.username,
        'email': temp_user.email,
    }


def test_read_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_get_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_get_user_not_found(client):
    response = client.get(f'/users/{randint(2, 10)}')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client, user, token, temp_user):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': user.username,
            'password': user.password,
            'email': temp_user.email,
            'id': user.id,
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': user.username,
        'email': temp_user.email,
        'id': user.id,
    }


def test_update_user_not_found(client, token, other_user, user):
    response = client.put(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': other_user.username,
            'password': other_user.password,
            'email': other_user.email,
            'id': user.id,
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}/', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client, token, other_user):
    response = client.delete(
        f'/users/{other_user.id}/', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_username_alredy_exists(client, user):
    user_schema = UserSchema.model_validate(user).model_dump()
    response = client.post(
        '/users/',
        json=user_schema,
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username alredy exists'}


def test_email_alredy_exists(client, user, temp_user):
    response = client.post(
        '/users/',
        json={
            'username': temp_user.username,
            'password': temp_user.password,
            'email': user.email,
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email alredy exists'}
