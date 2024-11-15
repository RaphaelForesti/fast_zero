from datetime import datetime, timedelta
from http import HTTPStatus

from freezegun import freeze_time

from fast_zero.schemas import UserSchemaTemp
from fast_zero.settings import Settings

settings = Settings()


def test_get_token(client, user):
    response = client.post(
        '/auth/token', data={'username': user.email, 'password': user.clean_password}
    )

    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token


def test_get_token_invalid_user(client, user):
    response = client.post(
        '/auth/token',
        data={'username': 'invalid_user', 'password': user.clean_password},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Incorrect username or password'}


def test_get_token_invalid_pass(client, user):
    response = client.post(
        '/auth/token', data={'username': user.username, 'password': 'fake_pass'}
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Incorrect username or password'}


def test_expired_token(client, user: UserSchemaTemp, temp_user: UserSchemaTemp):
    with freeze_time(datetime.now()):
        response = client.post(
            'auth/token', data={'username': user.email, 'password': user.clean_password}
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time(
        datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    ):
        response = client.put(
            f'/users/{user.id}',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'username': temp_user.username,
                'password': temp_user.password,
                'email': temp_user.email,
            },
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Expired credentials'}


def test_refresh_token(client, token):
    response = client.post(
        '/auth/refresh_token',
        headers={'Authorization': f'Bearer {token}'},
    )

    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in data
    assert 'token_type' in data
    assert data['token_type'] == 'Bearer'


def test_refresh_token_expired_time(client, user):
    with freeze_time(datetime.now()):
        response = client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time(
        datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    ):
        response = client.post(
            '/auth/refresh_token',
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Expired credentials'}
