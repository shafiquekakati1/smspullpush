import threading
import FINAL_UPDATE_R, FINAL_UPDATE_D
import time
import logging
logging.basicConfig(filename='/tmp/req_res.log', filemode='a',
                    format='%(asctime)s => %(name)s - %(levelname)s - %(message)s')
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

    # Use getconn() to Get Connection from connection pool
    ps_connection = postgreSQL_pool.getconn()


    
    if (ps_connection):
        print("successfully received connection from connection pool ")
        logging.info('postgreSQL_vfom.py - successfully received connection from connection pool ' + str(postgreSQL_pool))
        #PUT CODE HERE USING CONN ^

        while True:
          try:
            FINAL_UPDATE_D.DELIVERED_UPDATE(ps_connection)
            print('waiting for 30 seconds')
            time.sleep(30)
            FINAL_UPDATE_R.RESPONDED_UPDATE(ps_connection)
            time.sleep(30)
            print('waiting for 30 seconds')
          except Exception as ex:
            print('err while Updating D & R ' + str(ex))




    # Use this method to release the connection object and send back to connection pool
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

