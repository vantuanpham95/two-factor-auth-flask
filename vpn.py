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
 
 
def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None
 
 
def select_all_users(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
 
    rows = cur.fetchall()
 
    for row in rows:
        print(row)
 
 
def select_task_by_id(conn, id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id=?", (id,))
 
    rows = cur.fetchall()
 
    for row in rows:
        print(row)

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
        # print("1. Query user by id:")
        # select_task_by_id(conn,1)
 
        # print("2. Query all users")
        # select_all_users(conn)
 
 		# print("3. Check if user is exist")
 		# if username_is_exist(conn, "tuanpv") == True:
 		# # print(username_is_exist(conn, "tuanpv"))
 		# 	print("YEP")
 		# else:
 		# 	print("No")

 		# print("4. Select Hashed password")
 		# if username_is_exist(conn, "tuanpv"):
 		# 	print(select_hashed_passwd(conn, "tuanpv"))
 		# else:
 		# 	print("Username not exist!")

 		# print("6. Verify Password")
 		# print(verify_passwd(conn, "tuanpv", "1234"))

 		print("7. Select secret otp:")
 		print(select_otp_secret(conn, "tuanpv"))

 		print("8. Check verify otp:")
 		input_otp = input("Enter your 6 digits: ")
 		print(verify_otp(conn, "tuanpv", input_otp))

if __name__ == '__main__':
    main()