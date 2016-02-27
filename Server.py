#Server - 2/8/2016
#
import os
import socket
import threading
import json
import copy
import sqlite3
import lidtracking

from Globalconstants import *


# moved this to GlobalConstants
# Fixed port address for testing 
#PORT = 12345
#HOST = 'localhost'

# Constant replies
GENERAL_ERROR = ["NAK", 0 ]


# Dictionary of msg. handlers, items added below.
Handlers = {}
INVALID_REQUEST = ["NAK",0]

#-------------------------------------------------------------

def server_loop():

    # create the socket and listen
    srvsock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    srvsock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
    srvsock.bind(('', PORT) )# NOTE using '' instead of global host to bind to all interfaces
    srvsock.listen( 5 )

    while True:
        clisock, (remhost, remport) = srvsock.accept()
        rcv_string = clisock.recv(10240)
        if rcv_string == "":
            # ignore
            clisock.close()
            continue
        try:
            rcv_list = json.loads(rcv_string)
            request = rcv_list[0]
        except:
            # return general error
            logging.exception('server_loop list exception')
            logging.warning('server_loop list exception')
            logging.warning('    rcv: %s' % rcv_string)
            clisock.sendall(json.dumps(GENERAL_ERROR))
            clisock.close()
            continue
        #
        try:
            reply = Handlers[request](rcv_list)
        except:
            logging.exception('server_loop handler exception')
            logging.warning('server_loop handler exception')
            logging.warning('    rcv: %s' % rcv_string)
            reply = INVALID_REQUEST
        #
        clisock.sendall(json.dumps(reply))
        clisock.close()
        #
    # end while
#

Server = threading.Thread(target=server_loop, name="Server")
Server.daemon = True
_DataBase = None


def start_server():
    Server.start()
    
    
def persontojson(row):
	return [row.id,row.name,row.trained,row.role]
def persontonotes(row):
	return [row.id,row.name,row.notes]
def completepersontojson(row):
	return [row.id,row.name,row.trained,row.role,row.email,row.industry,row.created.strftime("%Y-%m-%d %H:%M:%S"),row.major,row.notes]
#-------------------------------------------------------------
# Handlers are all called with try:
# No need to catch exceptions here for general errors.

import Logging
import time



def GETVER(rcv):
     return ["ACK",VERSION,REVISION]
#
Handlers["GETVER"] = GETVER

def GETLISTUSER(rcv):
	rep = ["ACK"] 
	global _DataBase
	for row in _DataBase.GetUsers():
		rep.append(persontojson(row))
	return rep
#
Handlers["GETLISTUSER"] = GETLISTUSER

def GETREPORT(rcv):
	rep =["ACK"]
	global _DataBase
	for row in _DataBase.GetUsers():
		lst = [row.id,[]]
		for timerow in _DataBase.GetTimes(row.id):
			lst[1].append(persontojson(row))
		rep.append(lst)
	return rep		
#
Handlers["GETREPORT"] = GETREPORT
	
def GETUSER(rcv):
	rep=["ACK"]
	global _DataBase
	for row in _DataBase.GetUsers():
		if row.id == rcv[1]:
			if rcv[2] == 0:
				rep.append(persontojson(row))
			elif rcv[2] == 1:
				rep.append(persontonotes(row))
			elif rcv[2] ==2:
				rep.append(completepersontojson(row))
	return rep
Handlers["GETUSER"] = GETUSER

def UPDATEUSER(rcv):
	global _DataBase
	try:
		# --- id,name,email,industry,trained,role,major,notes
		_DataBase.EditUser(int(rcv[1]),rcv[2],rcv[3],rcv[4],int(rcv[5]),rcv[6],rcv[7],rcv[8])
		return ["ACK"]
	except:
		return GENERAL_ERROR
Handlers["UPDATEUSER"] = UPDATEUSER

def DELUSER(rcv):
	global _DataBase
	try:
		_DataBase.DelUser(int(rcv[1]))
		return ["ACK"]
	except:
		return GENERAL_ERROR
Handlers["DELUSER"] = DELUSER	
		
