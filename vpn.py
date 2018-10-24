#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import sqlite3
import os
import sys
import base64
import datetime
import config
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import onetimepass
 
debug = 0
 
def create_connection(db_file):
	try:
		conn = sqlite3.connect(db_file)
		return conn
	except Error as e:
		print(e)
 
	return None


def mylogger(message):
		timestamp=datetime.datetime.now().strftime('%a %b %e %H:%M:%S %Y us=%f')
		processname=__file__
		usrname=os.getenv('username')
		# usrname = "tuanpv"
		untrusted_ip = os.getenv('untrusted_ip')
		untrusted_port = os.getenv('untrusted_port')
		### OPENVPN LOGGING FORMAT
		print '{0} {4}:{5} cmd={1} username={2} {3}'.format(timestamp, processname, usrname, message, untrusted_ip, untrusted_port)
		return

def username_is_exist(conn, username):
	cur = conn.cursor()
	cur.execute("select id FROM users WHERE username=?",(username,))
	data = cur.fetchone()
	if data is None:
		return False
	else:
		# print("YEP")
		return True
 
def select_hashed_passwd(conn, username):
	cur = conn.cursor()
	cur.execute("select password_hash FROM users WHERE username=?", (username,))
	hassed_passwd = cur.fetchone()[0]
	return hassed_passwd

def verify_passwd(conn, username, password):
	return check_password_hash(select_hashed_passwd(conn, username), password)

def select_otp_secret(conn, username):
	cur = conn.cursor()
	cur.execute("SELECT otp_secret FROM users WHERE username=?", (username,))
	otp_secret = cur.fetchone()[0]
	return otp_secret

def verify_otp(conn, username, otp):
	return onetimepass.valid_totp(otp, select_otp_secret(conn, username))

def main():
	database = "db.sqlite"
 
	# create a database connection
	conn = create_connection(database)
	with conn:
		try:
				# usrname=os.getenv('username')
				# passwd =os.getenv('password')
				usrname = raw_input('username: ')
				passwd = raw_input('Enter passwd: ')
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
						mylogger(os.getresuid())
						for variable in os.environ:
								value = os.getenv(variable)
								mylogger('ENV {0}={1}'.format(variable,value))
						sys.exit(1)

		except Exception as e:
				mylogger(e)
				exit_val=1
		else:
				if verify_passwd(conn, usrname) and verify_otp(conn, usrname, otp):
						exit_val=0
						mylogger('HASH Access-Accept')
				else:
						exit_val=1
						mylogger('HASH Access-Reject')


		sys.exit(exit_val)

		### IF YOU FORGET TO SET exit_val DURING SCRIPT EXECUTION
		mylogger('ERROR: unexpected situation')
		### DENY ACCESS
		sys.exit(1)

if __name__ == '__main__':
	main()
