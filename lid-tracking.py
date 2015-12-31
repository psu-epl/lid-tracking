#!/usr/bin/env python
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from RPi import GPIO
import argparse
import time
import datetime
import threading

Base = declarative_base()

DATABASE_FILE = 'data.db'

reading = None

parser = argparse.ArgumentParser(description='L.I.D. User timestamp database')
parser.add_argument('--init', action="store_true", help='Initilize the database. WARNING: This can destroy data')
parser.add_argument('--report', action="store_true", help='Run a test report against the database')

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


def kick_timer():
    global reading
    if reading is None:
        threading.Timer(0.2, wiegand_stream_done).start()
        reading = 0

def leds_off():
    GPIO.output(27, GPIO.HIGH)

def wiegand_stream_done():
    global reading
    badgeno = (reading&0x0003fffe) >> 1
    reading = None

    # Check case for potentially garbage data
    if badgeno < 1000:
        return

    print "Badge Scaned: %7d" % badgeno

    engine = create_engine('sqlite:///'+DATABASE_FILE)
    Session = sessionmaker(bind=engine)
    session = Session()

    person =  session.query(Person).filter(Person.id == badgeno).first()
    if person is None:
        print "Hi! This is your first time scanning in."
        nameinput, emailinput, industryinput = ask_details()
        person = Person(id=badgeno, name=nameinput, email=emailinput, industry=industryinput)
        session.add(person)
        print "Thanks!"
        GPIO.output(27, GPIO.LOW)
    else:
        GPIO.output(27, GPIO.LOW)
    threading.Timer(0.35, leds_off).start()


    newcheckin = Timetable(person=person, timein=datetime.datetime.now())
    session.add(newcheckin)
    session.commit()


def ask_details():
    nameinput = str(raw_input('Please enter your name: '))
    emailinput = str(raw_input('Please enter your email: '))
    industryinput = str(raw_input('Please enter your Industry or Major: '))

    print "Hi", nameinput, "is this correct?:"
    print emailinput
    print industryinput
    yn = str(raw_input('[y/n] '))
    if 'n' in yn.lower():
        ask_details()
    return nameinput, emailinput, industryinput

# Initilize Database WARNING: Will destroy data
def init():
    engine = create_engine('sqlite:///'+DATABASE_FILE)
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    args = vars(parser.parse_args())

    if args['init']:
        if os.path.isfile(DATABASE_FILE):
            okay = raw_input("WARNING Overwrite database? [y/n] ") == 'y'
            if not okay:
                print "Aborting."
                exit(0)
        init()
        exit(0)


    if args['report']:
        engine = create_engine('sqlite:///'+DATABASE_FILE)
        Session = sessionmaker(bind=engine)
        session = Session()
        data = session.query(Person).all()
        for d in data:
            print d.id, d.name, d.industry
            for line in session.query(Timetable).filter(Timetable.person == d).all():
                print "    - Badgein:", line.timein
        exit(0)


    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23, GPIO.IN)
    GPIO.setup(24, GPIO.IN)
    GPIO.setup(27, GPIO.OUT)
    GPIO.output(27, GPIO.HIGH)
    GPIO.add_event_detect(23, GPIO.FALLING, callback=data_pulse)
    GPIO.add_event_detect(24, GPIO.FALLING, callback=data_pulse)


    while True:
        time.sleep(1000)


