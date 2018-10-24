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
		print("YEP")
		return True
 
def main():
    database = "db.sqlite"
 
    # create a database connection
    conn = create_connection(database)
    with conn:
        # print("1. Query user by id:")
        # select_task_by_id(conn,1)
 
        # print("2. Query all users")
        # select_all_users(conn)
 
 		print("3. Check if user is exist")
 		if username_is_exist(conn, "tuanpv") == True:
 			print("Yes")
 		print("No")
 
if __name__ == '__main__':
    main()