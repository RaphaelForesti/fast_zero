from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(username='foresti', email='foresti@teste.com.br', password='123456')
    session.add(user)
    session.commit()
    session.flush()
    result = session.scalar(select(User).where(User.email == 'foresti@teste.com.br'))

    assert result.username == 'teste_incorreto@teste.com'
