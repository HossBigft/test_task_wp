from sqlalchemy.orm import Session, scoped_session
from flask_bcrypt import Bcrypt
from typing import Dict, Any

from app.main import app
from app.db.models import User, Show


bcrypt = Bcrypt(app)


def get_user_by_name(*, session: Session, username: str) -> User | None:
    return session.query(User).filter(User.username == username).first()


def authenticate(*, session: Session, username: str, password: str) -> User | None:
    db_user = get_user_by_name(session=session, username=username)
    if db_user and bcrypt.check_password_hash(db_user.hashed_password, password):
        return db_user
    return None


def create_user(*, session: scoped_session, username: str, password: str) -> User:
    db_obj = User(
        username=username,
        hashed_password=bcrypt.generate_password_hash(password).decode("utf-8"),
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def search_movies(
    *, session: Session, filters: Dict[str, Any], limit: int = 10, offset: int = 0
):
    query = session.query(Show).filter(Show.type == "Movie")
    for field, value in filters.items():
        model_field = getattr(Show, field)
        if isinstance(value, str) and field in [
            "title",
            "description",
            "cast",
            "director",
            "country",
            "listed_in",
        ]:
            query = query.filter(model_field.ilike(f"%{value}%"))
        else:
            query = query.filter(model_field == value)

    return query.offset(offset).limit(limit).all()
