from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
import Person


Base = declarative_base()
class Timetable(Base):
    __tablename__ = 'timetable'
    id          = Column(Integer, primary_key=True)
    person_id   = Column(Integer, ForeignKey('person.id'))
    person      = relationship(Person)
    timein      = Column(DateTime, nullable=False)
