#### Logging.py 
# 2/20/2016 
# cody hanks 
# This file sets up the logging interface in python to keep rotating log files in the system 
# prevents large log file takeover of the system


import logging
from logging.handlers import RotatingFileHandler
import Globalconstants
# get global logger object 
global logger
# set loggger to default module logger 
logger = logging.getLogger(__name__)
# get a file handler object 
hnd = RotatingFileHandler(Globalconstants.LOGFILE, maxBytes=1000000, backupCount=5)
# set format for logs 
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# add the formatter
hnd.setFormatter(formatter)
# add the handler to the list 
logger.addHandler(hnd)
logger.setLevel(Globalconstants.LOGLEVEL)
# should prevent output to the screen from copying whats on logger
logger.propagate = False
