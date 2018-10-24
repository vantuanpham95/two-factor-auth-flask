#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import sqlite3 as lite
import os
import sys
import base64
import datetime
import config
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

debug = 0

# def mylogger(message):
#         timestamp=datetime.datetime.now().strftime('%a %b %e %H:%M:%S %Y')
#         processname=__file__
#         usrname=os.getenv('username')
#         untrusted_ip = os.getenv('untrusted_ip')
#         untrusted_port = os.getenv('untrusted_port')
#         ### OPENVPN LOGGING FORMAT
#         print '{0} {4}:{5} cmd={1} username={2} {3}'.format(timestamp, processname, usrname, message, untrusted_ip, untrusted_port)
# #        print 'abc'
#         return

def create_connection(db_file):
	try:
		conn = sqlite3.connect(db.file)
		return conn
	except Exception as e:
		# mylogger(e)
		exit_val = 1
	return None

def username_is_exist(conn, username):
	cur = conn.cursor()
	cur.execute("select id FROM users WHERE username = ?",(username,))
	data = cursor().fetchone()
	if data is None:
		return false
	else:
		return true

def select_hashed_passwd(conn, username):
	cur = conn.cursor()
	cur.execute("select password_hash FROM users WHERE username=?", (username,))
	hassed_passwd = cur.fetchall()
	return hassed_passwd

def select_secret_token(conn, username):
	cur = conn.cursor()
	cur.execute("select otp_secret FROM users WHERE username=?", (username,))
	secret_token = cur.fetchall()
	return secret_token

def verify_vpn(conn, username_input, password_input, otp_input):
	if username_is_exist:
		pass1 = select_hashed_passwd(conn, username)
		pass2 = generate_password_hash(password_input)
		if pass1 == pass2:
			exit_val = 0
			mylogger('Passwd acepted!')
	else:
		exit_val = 1
		# mylogger("Username doesn't exist!")

try:
#        usrname=os.getenv('username')
#        passwd =os.getenv('password')
        usrname = input('Enter username: ')
        passwd = input('Enter passwd: ')
        otp=passwd[:6]
        real_passwd=passwd[6:]

        if usrname is None:
                myerr=('username is missing')
                raise Exception(myerr)

        if passwd is None:
                myerr=('password is missing')
                raise Exception(myerr)

        ### IF DEBUGGING IS ON THEN WE DENY ACCESS TO ALL USERS!
        if debug == 1:
                # mylogger(os.getresuid())
                for variable in os.environ:
                        value = os.getenv(variable)
                        # mylogger('ENV {0}={1}'.format(variable,value))
                sys.exit(1)

except Exception as e:
        # mylogger(e)
        exit_val=1
else:
		db_file = "/root/git/two-factor-auth-flask/db.sqlite"
		conn = create_connection(db_file)
		with conn:
			verify_vpn(conn, usrname, real_passwd, otp)
#     	user = app.User.query.filter_by(username=usrname).first()
#         if user is None or not user.verify_password(real_passwd) or not user.verify_totp(otp):
#                 print 'Khong thay user'
#                 exit_val = 1
#                 mylogger('OTP Access-Reject')
# #        print()
#         exit_val=0
#         mylogger('OTP Access-Accept')

sys.exit(exit_val)

### IF YOU FORGET TO SET exit_val DURING SCRIPT EXECUTION
# mylogger('ERROR: unexpected situation')
### DENY ACCESS
sys.exit(1)