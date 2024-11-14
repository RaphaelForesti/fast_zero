from http import HTTPStatus


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
