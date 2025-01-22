import uuid
from sqlalchemy import Column, Integer, String, Text, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()


class Show(Base):
    __tablename__ = "shows"

    show_id = Column(Text, primary_key=True)
    type = Column(String(50))
    title = Column(String(200))
    director = Column(Text)
    cast = Column(Text)
    country = Column(Text)
    date_added = Column(Date)
    release_year = Column(Integer)
    rating = Column(String(10))
    duration = Column(String(20))
    listed_in = Column(Text)
    description = Column(Text)


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(20), unique=True, nullable=False)
    hashed_password = Column(String(80), nullable=False)
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<User {self.username}>"
