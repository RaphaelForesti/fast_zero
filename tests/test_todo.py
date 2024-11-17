from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.models import TodoState
from tests.conftest import TodoFactory

endpoint = '/todos'


def get_headers(p_token):
    return {'Authorization': f'Bearer {p_token}'}


def test_create_todo(client: TestClient, token):
    response = client.post(
        endpoint,
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'titulo teste',
            'description': 'descrição teste',
            'state': 'draft',
        },
    )
    assert response.status_code == HTTPStatus.CREATED


def test_list_should_return_5_todos(db_session, client, token, user):
    expected_todos = 5
    db_session.bulk_save_objects(
        TodoFactory.create_batch(expected_todos, user_id=user.id)
    )
    db_session.commit()

    response = client.get(endpoint, headers=get_headers(p_token=token))

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


def test_list_todos_pagination_should_return_2_todos(db_session, client, token, user):
    expected_todos = 2
    db_session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id))
    db_session.commit()

    response = client.get(
        f'{endpoint}/?offset=1&limit={expected_todos}',
        headers=get_headers(p_token=token),
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


def test_list_todos_title_should_return_5_todos(db_session, client, token, user):
    expected_todos = 5
    db_session.bulk_save_objects(
        TodoFactory.create_batch(5, user_id=user.id, title='Teste Todo 1')
    )
    db_session.commit()

    response = client.get(
        f'{endpoint}/?title=Teste', headers=get_headers(p_token=token)
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


def test_list_todos_description_should_return_5_todos(db_session, client, token, user):
    expected_todos = 5
    db_session.bulk_save_objects(
        TodoFactory.create_batch(
            5, user_id=user.id, description='minha teste descricao'
        )
    )
    db_session.commit()

    response = client.get(
        f'{endpoint}/?description=descr', headers=get_headers(p_token=token)
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


def test_list_todos_sate_should_return_5_todos(db_session, client, token, user):
    expected_todos = 5
    db_session.bulk_save_objects(
        TodoFactory.create_batch(5, user_id=user.id, state=TodoState.draft)
    )
    db_session.commit()

    response = client.get(
        f'{endpoint}/?state=draft', headers=get_headers(p_token=token)
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


def test_list_todos_filter_combined_should_return_5_todos(
    db_session, client, token, user
):
    expected_todos = 5
    db_session.bulk_save_objects(
        TodoFactory.create_batch(
            5,
            user_id=user.id,
            state=TodoState.done,
            title='Teste todo done',
            description='Teste todo done',
        )
    )

    db_session.bulk_save_objects(
        TodoFactory.create_batch(
            5,
            user_id=user.id,
            state=TodoState.trash,
            title='Teste todo trash',
            description='Teste todo trash',
        )
    )
    db_session.commit()

    response = client.get(
        f'{endpoint}/?state=done&title=done&description=done',
        headers=get_headers(p_token=token),
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


def test_list_todos_filter_combined_should_return_2_limit_todos(
    db_session, client, token, user
):
    expected_todos = 2
    db_session.bulk_save_objects(
        TodoFactory.create_batch(
            5,
            user_id=user.id,
            state=TodoState.done,
            title='Teste todo done',
            description='Teste todo done',
        )
    )

    db_session.bulk_save_objects(
        TodoFactory.create_batch(
            5,
            user_id=user.id,
            state=TodoState.trash,
            title='Teste todo trash',
            description='Teste todo trash',
        )
    )
    db_session.commit()

    response = client.get(
        f'{endpoint}/?state=done&title=done&description=done&limit=2',
        headers=get_headers(p_token=token),
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


def test_delete_todo(db_session, client, token, user):
    todo = TodoFactory(user_id=user.id)
    db_session.add(todo)
    db_session.commit()

    response = client.delete(
        f'{endpoint}/{todo.id}', headers=get_headers(p_token=token)
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Task has been deleted successfuly'}


def test_delete_todo_task_not_found(db_session, client, token, user):
    todo = TodoFactory(user_id=user.id)
    db_session.add(todo)
    db_session.commit()

    response = client.delete(f'{endpoint}/{5}', headers=get_headers(p_token=token))

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_patch_todo_task_not_found(client, token):
    response = client.patch(
        f'{endpoint}/{5}', headers=get_headers(p_token=token), json={}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found.'}


def test_patch_todo(db_session, client, token, user):
    todo = TodoFactory(user_id=user.id)
    db_session.add(todo)
    db_session.commit()
    db_session.refresh(todo)

    response = client.patch(
        f'{endpoint}/{todo.id}',
        headers=get_headers(p_token=token),
        json={'title': 'Teste!'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['title'] == 'Teste!'
