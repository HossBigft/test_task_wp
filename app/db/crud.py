from sqlalchemy.orm import Session, scoped_session
from sqlalchemy import func, or_
from flask_bcrypt import Bcrypt
from typing import Dict, Any, Callable


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


def search_shows(
    *, session: Session, filters: Dict[str, Any], limit: int = 10, offset: int = 0
):
    search_querys: Dict[str, Callable] = {
        "exact": lambda field, value: field == value,
        "search_text": lambda field, value: field.ilike(f"%{value}%"),
        "search_text_array": lambda field, value: or_(
            *[func.array_to_string(field, ",").ilike(f"{v}%") for v in value]
        ),
        "exact_text": lambda field, value: field.ilike(value),
    }

    column_search_actions: Dict[str, str] = {
        "type": "exact_text",
        "title": "search_text",
        "director": "search_text_array",
        "rating": "exact_text",
        "cast": "search_text_array",
        "country": "search_text_array",
        "date_added": "exact",
        "release_year": "exact",
        "duration": "search_text",
        "listed_in": "search_text_array",
        "description": "search_text",
    }

    query = session.query(Show)

    for field, value in filters.items():
        model_field = getattr(Show, field)
        column_search_action = column_search_actions.get(field, "exact")
        action = search_querys[column_search_action]
        query = query.filter(action(model_field, value))

    return query.offset(offset).limit(limit).all()
