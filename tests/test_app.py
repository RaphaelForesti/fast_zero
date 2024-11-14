from http import HTTPStatus


def test_read_root_retornar_ok_ola_mundo(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá mundo'}
