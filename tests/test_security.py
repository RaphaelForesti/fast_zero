from http import HTTPStatus

from fastapi.testclient import TestClient
from jwt import decode

from fast_zero.security import create_access_token, settings


def test_jwt(user):
    data = {'sub': user.email}
    token = create_access_token(data=data)

    result = decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    assert result['sub'] == data['sub']
    assert result['exp']


def test_jwt_invalid_token(client: TestClient, user):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': 'Bearer token-invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
