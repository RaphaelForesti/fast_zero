from http import HTTPStatus


def test_read_root_retornar_ok_ola_mundo(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá mundo'}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'testeuser',
            'password': 'password',
            'email': 'email@teste.com',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'testeuser',
        'email': 'email@teste.com',
    }


def test_read_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [{'id': 1, 'username': 'testeuser', 'email': 'email@teste.com'}]
    }


def test_get_user(client):
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'testeuser',
        'email': 'email@teste.com',
    }


def test_get_user_not_found(client):
    response = client.get('/users/100')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client):
    response = client.put(
        '/users/1/',
        json={
            'username': 'alterado',
            'password': 'password',
            'email': 'email@teste.com',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'alterado',
        'email': 'email@teste.com',
    }


def test_update_user_not_found(client):
    response = client.put(
        '/users/100/',
        json={
            'username': 'alterado',
            'password': 'password',
            'email': 'email@teste.com',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client):
    response = client.delete('/users/1/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client):
    response = client.delete('/users/100/')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
