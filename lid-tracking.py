#!/usr/bin/env python
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from RPi import GPIO
import argparse
import time
import threading

Base = declarative_base()

DATABASE_FILE = 'data.db'

reading = None

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


def data_pulse(arg):
    global reading
    kick_timer()
    if arg == 23:
        reading = reading << 1
        reading += 1
    if arg == 24:
        reading = reading << 1
        #reading += 1


def kick_timer():
    global reading
    if reading is None:
        threading.Timer(0.2, wiegand_stream_done).start()
        reading = 0

def wiegand_stream_done():
    global reading
    print "Badge number: %7d" % ((reading&0x0003fffe) >> 1)
    reading = None


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

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23, GPIO.IN)
    GPIO.setup(24, GPIO.IN)
    GPIO.add_event_detect(23, GPIO.FALLING, callback=data_pulse)
    GPIO.add_event_detect(24, GPIO.FALLING, callback=data_pulse)


    while True:
        time.sleep(1000)


