from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import Message, UserList, UserPublic, UserSchema

app = FastAPI()

database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá mundo'}


@app.post('/users', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )
    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail='Username alredy exists'
            )
        elif db_user.email == db_user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail='Email alredy exists'
            )
    db_user = User(username=user.username, email=user.email, password=user.password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@app.get('/users', status_code=HTTPStatus.OK, response_model=UserList)
def read_users(
    limit: int = 50, offset: int = 0, session: Session = Depends(get_session)
):
    users = session.scalars(select(User).limit(limit).offset(offset))
    return {'users': users}


@app.get('/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user_whith_id = session.scalar(select(User).where(User.id == user_id))
    if not user_whith_id:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')
    return user_whith_id


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):
    user_whith_id = session.scalar(select(User).where(User.id == user_id))
    if not user_whith_id:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    user_whith_id.email = user.email
    user_whith_id.username = user.username
    user_whith_id.password = user.password
    session.add(user_whith_id)
    session.commit()

    return user_whith_id


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user_whith_id = session.scalar(select(User).where(User.id == user_id))
    if not user_whith_id:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    session.delete(user_whith_id)
    session.commit()
    return {'message': 'User deleted'}
