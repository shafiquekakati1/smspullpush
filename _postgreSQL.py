import threading
import FINAL_UPDATE_R, FINAL_UPDATE_D
import time
import logging
logging.basicConfig(filename='/tmp/req_res_log.log', filemode='a', format='%(asctime)s => %(name)s - %(levelname)s - %(message)s')
import psycopg2
from psycopg2 import Error
import pandas as pd
from psycopg2 import pool
import warnings
warnings.simplefilter("ignore", UserWarning)






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
        
    def getConnection():
        ps_connection = postgreSQL_pool.getconn()
        return ps_connection


    def putConnection(ps_connection):
        postgreSQL_pool.putconn(ps_connection)
        print("Put away a PostgreSQL connection")
        logging.info('postgreSQL_vfom.py - Put away a PostgreSQL connection ' + str(postgreSQL_pool))


except (Exception, psycopg2.DatabaseError) as error:
    print("Error while connecting to PostgreSQL", error)
    logging.error('postgreSQL_vfom.py - Error while connecting to PostgreSQL ' + str(error))

finally:
    # closing database connection.
    # use closeall() method to close all the active connection if you want to turn of the application
    if postgreSQL_pool:
        postgreSQL_pool.closeall
    print("PostgreSQL connection pool is closed")
    logging.info('postgreSQL_vfom.py - PostgreSQL connection pool is closed ' + str(postgreSQL_pool))

