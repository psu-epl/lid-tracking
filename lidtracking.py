	#!/usr/bin/env python
# lid-tracking.py -- Cody Hanks  based on file from Kris Clark 
# 2/8/2016 - 
# This is the main program and thread initializer file for lid-tracking

import os
import sys
import logging
import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
import Globalconstants
########################################################################
import DataBase
_DataBase = DataBase.DataBase()
####################################### Setup Database 
from Logging import logger

import argparse
import time
import datetime
import threading
import Server
import Gui
import RPi.GPIO as GPIO

from time import sleep
#command line arguments 
parser = argparse.ArgumentParser(description='L.I.D. User timestamp database')
parser.add_argument('--init', action="store_true", help='Initilize the database. WARNING: This can destroy data')
parser.add_argument('--report', action="store_true", help='Run a test report against the database')
parser.add_argument('--debug', action="store_true",help='Set log level to Debug')
########################################################################

reading =None
unknownusercallback = None
knownusercallback = None



def checkgoodreading():
	global reading
	global knownusercallback
	global unknownusercallback
	global _DataBase

	badgeno = (reading & 0x000fffff)>>1
	reading = None
	
        	
	if badgeno <1000:
		return 
	if badgeno >9999999:
		return 
		
	logger.debug('badge scanned: %7d'%badgeno)
	found = False
	for row in _DataBase.GetUsers():
		if row.id == badgeno:
			pers = persontojson(row)
			found = True
	if found:
		_DataBase.DelNotes(pers[0])
		_DataBase.AddTime(pers[0],datetime.datetime.now())
		#UserClockRecord(self,notes,id,name):
		knownusercallback(str(pers[2]),pers[0],str(pers[1]))
	else:
		unknownusercallback(badgeno)


def persontojson(row):
	return [row.id,row.name,row.usernotes]

def data_pulse(arg):
	global reading
	if reading == None:
		reading = 0
		threading.Timer(.5, checkgoodreading).start()
	if arg == 23:
		reading = reading <<1
		reading += 1
	if arg == 24:
		reading = reading <<1


########################################################################
## main 
def main():
	# get cmd line args 
	args = vars(parser.parse_args())
	logger.debug('args: '+str(args))
	
	# obvious ..... 
	if args['debug']:
		logger.setLevel(logging.DEBUG)
	
    # Log main function and program start 
	logger.warning('LID Tracking started')
	print 'LID Tracking'

	global _DataBase
    # if database not exists then create it...
	if not os.path.exists(Globalconstants.DATABASE_FILE):
		_DataBase.New_DB_Create()
		_DataBase.Try_Connect()
	else:
		if not _DataBase.Try_Connect():
			exit
	#set server Database 
	#Server._DataBase = _DataBase
	#start server 
	Server.start_server()
	
	global knownusercallback
	global unknownusercallback 

	# gui init group sets up the screen for gui 
	root=Gui.tk.Tk()
	app=Gui.FullScreenApp(root)
	Gui.root = root
	# set the gui new user call back function .... 
		#NewUser(self,_id,_name,_email,_industry):
	app.setnewusercallback(_DataBase.NewUser)
	# get the callback function for unknown user callback
		#Unknownusercallback(self,_id):
	unknownusercallback = app.getunknownusercallback(root)
	# set the delnote call back 
	app.setdelnotecallback(_DataBase.DelNotes)
	# get the callback function for clock record
		#UserClockRecord(self,notes,id,name)
	knownusercallback = app.getknownusercallback(root)

	GPIO.setmode(GPIO.BCM)
	GPIO.setup(23, GPIO.IN)
	GPIO.setup(24, GPIO.IN)	
	GPIO.add_event_detect(23, GPIO.FALLING, callback=data_pulse)
	GPIO.add_event_detect(24, GPIO.FALLING, callback=data_pulse)

	
	
	#thread = threading.Thread(target=unknownusercallback,args=[155802])
	#thread.start()
	# start the gui .... note if gui is closed program will stop 
	# while loop should restart gui in case it is closed 
	#while(True):
	
	#print _DataBase.EditUser(1,"Name","email","indus",0,"role","major","notes")
	
	
	root.mainloop()

#global unknownusercallback
#global knownusercallback
#global reading 
#reading =None
#unknownusercallback = None
#knowncusercallback = None

# caller for main 
if __name__ == '__main__': 
	main()
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	##### Archive dead code 
	
	
	
	#DT = DataBase.Timetable(
	#person_id=10001,
	#timein=datetime.datetime.now())
	#_DataBase.session.add(DT)
	
	#p = DataBase.Person(id=10001,name='Default',email='none@somedomain.com',industry='ComputerEngineering')
	#DB.session.add(p)
	#DB.session.commit()
	#q=DB.GetUsers()
	#print q
	#q= DB.session.query(person)
	#print q
    
    #GPIO.setmode(GPIO.BCM)
    #GPIO.setup(23, GPIO.IN)
    #GPIO.setup(24, GPIO.IN)
    #GPIO.setup(27, GPIO.OUT)
    #GPIO.setup(RED_LED, GPIO.OUT)
    #GPIO.output(27, GPIO.HIGH)
    #GPIO.output(RED_LED, GPIO.HIGH)
    #GPIO.add_event_detect(23, GPIO.FALLING, callback=data_pulse)
    #GPIO.add_event_detect(24, GPIO.FALLING, callback=data_pulse)


