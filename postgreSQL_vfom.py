import psycopg2
from psycopg2 import Error
import pandas as pd
from psycopg2 import pool
import warnings
warnings.simplefilter("ignore", UserWarning)
import logging
logging.basicConfig(filename='/tmp/req_res.log', filemode='a',
                    format='%(asctime)s => %(name)s - %(levelname)s - %(message)s')






def select(cmd, ps_connection):
    try:
        ps_cursor = ps_connection.cursor()
        ps_cursor.execute(cmd)
        ps_connection.commit()
        print("Displaying rows from mobile table")
        return pd.read_sql_query(cmd, ps_connection)
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
        logging.error('postgreSQL_vfom.py - Error while connecting to PostgreSQL ' + str(error))
    
def insert(cmd, ps_connection):
    try:
        ps_cursor = ps_connection.cursor()
        ps_cursor.execute(cmd)
        ps_connection.commit()
        ps_cursor.close()
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
        logging.error('postgreSQL_vfom.py - Error while connecting to PostgreSQL ' + str(error))

def update(cmd, ps_connection):
    try:
        ps_cursor = ps_connection.cursor()
        ps_cursor.execute(cmd)
        ps_connection.commit()
        ps_cursor.close()
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)   
        logging.error('postgreSQL_vfom.py - Error while connecting to PostgreSQL ' + str(error))         

def delete(cmd, ps_connection):
    try:
        ps_cursor = ps_connection.cursor()
        ps_cursor.execute(cmd)
        ps_connection.commit()
        ps_cursor.close()
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)   
        logging.error('postgreSQL_vfom.py - Error while connecting to PostgreSQL ' + str(error))  




