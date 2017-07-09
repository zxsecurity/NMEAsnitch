#!/usr/bin/env python3
# coding=utf-8

"""
nmeasnitch.py is tool that will try and detect if the GPS is being spoofed. 

command:
    nemasnitch.py
    
The configuration of the checking is handled by nemasnitch.cfg and the logging configuarion by logging.cfg
"""

__author__ = 'Karit @nzkarit'
__copyright__ = 'Copyright 2017 Karit'
__license__ = 'MIT'
__version__ = '0.1'

import serial
import sqlite3
import configparser
import logging
import logging.config
import datetime

def read_serial():
    while True:
        line = str(ser.readline())
        ts = str(datetime.datetime.now())
        tidied = line.strip("b'").strip("\\r\\n")
        
        if tidied[:1] == '$':
            if log_to_db:
                sentence_type = tidied.split(",")[0]
                c = conn.cursor()
                c.execute('INSERT INTO sentences (date, sentence, sentence_type) VALUES (?, ?, ?)', (ts, tidied, sentence_type))
                conn.commit()
                c.close()
            logger.debug(tidied)

def start_serial():
    serial_port = cfg.get('serial' , 'serial_port')
    logger.debug('Starting Serial connection to %s'%(serial_port))
    global ser
    ser = serial.Serial(serial_port, timeout=1)

def close_serial():
    logger.debug('Closing Serial connection')
    ser.close()

def connect_to_db():
    """
    Connect to the sqlite database
    
    The configuartion for this is gpsnitch.cfg
    """
    global log_to_db
    log_to_db = cfg.getboolean('database', 'log_to_db')
    if log_to_db:
        logger.debug('Connecting to DB')
        global conn 
        filename = cfg.get('database' , 'db_filename')
        conn = sqlite3.connect(filename)
        logger.debug('Connected to DB')
    else:
        logger.debug('Not Logging to DB')

def close_db():
    if log_to_db:
        logger.debug('Closing DB')
        conn.close()
    else:
        logger.debug('Not Logging to DB, so nothing to close')    

def shut_down():
    """
    Closes connections
    """
    close_db()
    close_serial()

def start_script():
    global cfg
    cfg = configparser.ConfigParser()
    cfg.read('nmeasnitch.cfg')
    
    global logger
    logging.config.fileConfig('logging.cfg')
    logger = logging.getLogger(__name__)
    logger.info('Starting nmeasnitch')
    
    start_serial()
    connect_to_db()
    
    try:
        read_serial()
    except KeyboardInterrupt:
        shut_down()
    except (OSError, IOError) as error:
        shut_down()
        sys.stderr.write('\rError--> {}'.format(error))
        logger.error('Error--> {}'.format(error))
        sys.exit(1) 

if __name__ == '__main__':
    start_script()
