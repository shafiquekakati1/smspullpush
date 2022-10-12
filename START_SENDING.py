# CHECK JOB TABLE FOR STATUS = READY_SEND
import sqlFunctions
import sender
import pandas as pd
import logging
logging.basicConfig(filename='/tmp/req_res.log', filemode='a',
                    format='%(asctime)s => %(name)s - %(levelname)s - %(message)s')
import psycopg2
from psycopg2 import Error
import pandas as pd
from psycopg2 import pool
import warnings
warnings.simplefilter("ignore", UserWarning)




#API WILL CHECK THE JOB, PICK UP THE JOBS, SEND FOR EACH ENTRY IN JOB DETAILS,





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
        df = sqlFunctions.CHECK_READY_SEND(ps_connection)

        id = df.loc[0][0]
        status = df.loc[0][1]
        creation_timestamp = df.loc[0][2]
        finished_timestamp = df.loc[0][3]
      
        if 'READY_SEND' in status:
            print('Ready to send SMSs for Job ID : ' + id)
            dfMSISDN = sqlFunctions.GET_MSISDN_WHERE_READY(ps_connection, id)
            print(dfMSISDN)
            sqlFunctions.UPDATE_STATUS_IN_JOB(ps_connection, id, 'SENDING')
            for index, row in dfMSISDN.iterrows():
                print(row[2], row[3])
                #SEND SMS       
                #AND UPDATES THE STATUS STARTED SENDING, 
                #  FOR EACH MSISDN WILL BE UPDATED WITH SEQ NUMBER
                sqlFunctions.UPDATE_STATUS_IN_JOB_DETAILS(ps_connection, id, row[2], 'STARTED_SENDING')
                print('\n\n')
                sqlFunctions.UPDATE_SEQ_NUM_IN_JOB_DETAILS(ps_connection, id, row[2], sender.start_sending(row[3].encode("utf-8"), row[2]))
                sqlFunctions.UPDATE_JOB_STATUS(ps_connection, id,'DONE')
        





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



# RESPONSE WILL
