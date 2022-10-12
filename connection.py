#!/bin/python3

import psycopg2
from psycopg2 import Error
from psycopg2 import pool
import logging
import time

logging.basicConfig(filename='/tmp/req_res.log', filemode='a',format='%(asctime)s => %(name)s - %(levelname)s - %(message)s')

username = 'sms_user'
password = '!Vfoman@009988'
hostname = '10.14.12.187'
port = '5432'
database = 'bulksmssend'

try:
	postgreSQL_pool = pool.SimpleConnectionPool(1, 20, user=username,
                                                password=password,
                                                host=hostname,
                                                port=port,
                                                database=database)
	if (postgreSQL_pool):
		print("Connection pool created successfully")
		logging.info('postgreSQL_vfom.py - Connection pool created successfully ' + str(postgreSQL_pool))

	# Use getconn() to Get Connection from connection pool
	ps_connection = postgreSQL_pool.getconn()

	if (ps_connection):
		print("successfully received connection from connection pool ")
		logging.info('postgreSQL_vfom.py - successfully received connection from connection pool ' + str(postgreSQL_pool))
	
	postgreSQL_pool.putconn(ps_connection)
