from sqlalchemy import select

from fast_zero.models import User


def test_create_user(db_session):
    user = User(username='foresti', email='foresti@teste.com.br', password='123456')
    db_session.add(user)
    db_session.commit()
    db_session.flush()
    result = db_session.scalar(select(User).where(User.email == 'foresti@teste.com.br'))

    assert result.username == 'foresti'
