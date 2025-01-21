from sqlalchemy import Column, Integer, String, Text, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Movie(Base):
    __tablename__ = "movies"

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

