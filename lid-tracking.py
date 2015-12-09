#!/usr/bin/env python
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import argparse

Base = declarative_base()

DATABASE_FILE = 'data.db'

parser = argparse.ArgumentParser(description='L.I.D. User timestamp database')
parser.add_argument('--init', action="store_true", help='Initilize the database. WARNING: This can destroy data')


class Person(Base):
    __tablename__ = 'person'
    id          = Column(Integer, primary_key=True)
    name        = Column(String(250), nullable=False)
    email       = Column(String(250), nullable=False)
    industry    = Column(String(250), nullable=False)


class Timetable(Base):
    __tablename__ = 'timetable'
    id          = Column(Integer, primary_key=True)
    person_id   = Column(Integer, ForeignKey('person.id'))
    person      = relationship(Person)
    timein      = Column(DateTime, nullable=False)


# Initilize
def init():
    engine = create_engine('sqlite:///'+DATABASE_FILE)
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    args = vars(parser.parse_args())
    print args

    if args['init']:
        if os.path.isfile(DATABASE_FILE):
            okay = raw_input("WARNING Overwrite database? [y/n] ") == 'y'
            if not okay:
                print "Aborting."
                exit(0)
        init()
