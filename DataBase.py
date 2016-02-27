######  Database.py 
#2/20/2016 
# Cody Hanks 

from sqlalchemy.dialects import mysql
from sqlalchemy import update
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
import datetime
import Globalconstants
from Logging import logger
# needed for sql alchemeny
Base = declarative_base()
i = 0;
def defaultid():
	global i
	i += 1
	return i
# class for table person this will define the Database as well as create user object 
# for passing between elements 
class Person(Base):
	__tablename__ = 'person'
	id          = Column(Integer, primary_key=True, autoincrement=False)
	name        = Column(String(250), nullable=False)
	email       = Column(String(250), nullable=False)
	industry    = Column(String(250), nullable=False)
	trained 	= Column(Integer, nullable=False) # Bit coded  
		# bit 0 = Stratasys Mojo 3D printer (FDM)
		# bit 1 = Spectrum Engineering Laser Pro24x12
		# bit 2 = LPKF S63 Printed Circuit Board Router
		# bit 3 = AccurateCNC A406 Printed Circuit Board Router
		# bit 4 = LPKF MiniContact-RS plating tank
		# bit 5 = Soldering Equipment
		# bit 6 = Torch T200N+ reflow oven
		# bit 7 = Misc Hand tools, including drill press, saws, etc.
	role		= Column(String(250), nullable=False)
	created 	= Column(DateTime, nullable=False)
	major		= Column(String(250), nullable=False)
	notes		= Column(mysql.TEXT(charset='unicode'),nullable=False)
	usernotes	= Column(mysql.TEXT(charset='unicode'),nullable=False)
	def __str__(self):
		return str(self.id)+self.name+self.email+self.industry+role+created+major+notes
	

## Class for table in Time table 
class Timetable(Base):
    __tablename__ = 'timetable'
    id          = Column(Integer, primary_key=True)
    person_id   = Column(Integer, ForeignKey('person.id'))
    person      = relationship(Person)
    timein      = Column(DateTime, nullable=False)


## Data base class to initialize the DB and keep the table for all threads 
class DataBase():
	
	engine = None
	session = None
	## init sets the DB file from Global consts.
	def __init__(self):
		self.engine = create_engine('sqlite:///'+Globalconstants.DATABASE_FILE)
	
	# will create a new file and log that it was created
	def New_DB_Create(self):
		logger.warning('New DataBase File Created')
		Base.metadata.create_all(self.engine)

	# try to connect to the DB 
	def Try_Connect(self):
		try:
			logger.warning('Connecting session to DB file'+Globalconstants.DATABASE_FILE)
			Base.metadata.bind = self.engine
			Session = sessionmaker(bind=self.engine)
			self.session = Session()
		except:
			logger.exception('Exeption connecting to session for DB.file:'+Globalconstants.DATABASE_FILE)
			raise # rerais exception for program 
	
	
	# add a new person 
	def AddUser(self,Person):
		self.session.add(Person)
		self.session.commit()

	# get users list 
	def GetUsers(self):
		return self.session.query(Person).all()
	
	# get time table by person ID # note if DB gets large this is to keep total query size down
	# there should be no query to return the entire table at once.
	def GetTimes(self,Pid):
		return self.session.query(Timetable).filter(Timetable.person_id==Pid)
	
	# new user callback create a new user from items 
	def NewUser(self,_id,_name='',_email='',_industry='',_trained = 0,_role='user',_major='',_notes='',_usernotes=''):			
		p = Person(id=int(_id),name=_name,email=_email,industry=_industry,trained=_trained,role=_role,created=datetime.datetime.now(),major=_major,notes=_notes,usernotes=_usernotes)
		try:
			self.session.add(p)
			logger.debug('Added user id %d'%int(_id))
			logger.debug('user name %s'%_name)
			self.session.commit()
		except:
			self.session.rollback()
			logger.debug('  user id %d'%int(_id))
			logger.debug(' name %s'%_name)
			logger.debug(' email %s'%_email)
			logger.debug(' ind %s'%_industry)
			logger.debug('trained %d'%_trained)
			logger.debug(' role %s'%_role)
			logger.debug(' major %s'%_major)
			logger.debug(' notes %s'%_notes)
			raise Exception("Unable to add user please check input")
	
	# edit a user 
	def EditUser(self,_id,_name,_email,_industry,_trained,_role,_major,_notes,_usernotes):
		self.session.query(Person).\
			filter(Person.id ==_id).\
			update({ 'name':_name,'email':_email,'industry':_industry,'trained':_trained,'role':_role,'major':_major,'notes':_notes,'usernotes':_usernotes})
		self.session.commit()
		
	def DelUser(self,_id):
		self.session.query(Person).\
			filter(Person.id == _id).\
			delete()
		self.session.commit()
		
		
	#Add Time Record 
	def AddTime(self,_id,_time):
		tm = Timetable(_id,_time)
		try:
			self.session.add(tm)
			self.session.commit()
		except:
			logger.debug('unable to add time record')
	
	def DelNotes(self,_id):
		pass
