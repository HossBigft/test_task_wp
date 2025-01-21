from sqlalchemy import select
from flask_bcrypt import check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from app.main import app

from app.db.models import User


bcrypt = Bcrypt(app)


def get_user_by_email(*, session: SQLAlchemy, username: str) -> User | None:
    statement = select(User).where(User.username == username)
    session_user = session.exec(statement).first()
    return session_user


def authenticate(*, session: SQLAlchemy, username: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, username=username)
    if not db_user:
        return None
    if not check_password_hash(password, db_user.hashed_password):
        return None
    return db_user


def create_user(*, session: SQLAlchemy, username: str, password: str) -> User:
    db_obj = User(
        username=username,
        hashed_password=bcrypt.generate_password_hash(password).decode("utf-8"),
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj
