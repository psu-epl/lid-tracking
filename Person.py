from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine





class Person(object):
	__tablename__ = 'person'
	id          = Column(Integer, primary_key=True)
	name        = Column(String(250), nullable=False)
	email       = Column(String(250), nullable=False)
	industry    = Column(String(250), nullable=False)

	#def __init__(self,id,name,email,industry):
	#	self.id = id
	#	self.name = name
	#	self.email = email 
	#	self.industry = industry

