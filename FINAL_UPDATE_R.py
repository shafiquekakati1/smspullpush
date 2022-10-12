import sqlFunctions
import pandas as pd
from datetime import datetime, timedelta
import time
import logging
logging.basicConfig(filename='/tmp/req_res.log', filemode='a',
                    format='%(asctime)s => %(name)s - %(levelname)s - %(message)s')

#RESPONDED
def RESPONDED_UPDATE(ps_connection):
    try:
        RES_DF = sqlFunctions.GET_TRANSITION(ps_connection, 'response','response')

        currentTimeStamp = datetime.now()
        minus24Hours = currentTimeStamp - timedelta(days=1)

        jobDetailsDF = sqlFunctions.GET_JOB_DETAILS_TO_UPDATE_SEQUENCE(ps_connection)

        print(RES_DF)
        for indexD, rowD in jobDetailsDF.iterrows():
            if 'SENT' in rowD[6] and 'DELIVRD' in rowD[8]:
                for index, row in RES_DF.iterrows():
                    if row[6] >  minus24Hours < currentTimeStamp and  rowD[2]==row[2] :
                        sqlFunctions.UPDATE_RESPONSE_IN_JOB_DETAILS(ps_connection, rowD[0], rowD[2], row[1], 'RESPONDED',row[3])     
                        sqlFunctions.UPDATE_TRANSITION_STATUS(ps_connection, row[1],'DONE')                           
            else:
                print('no work to do R ')
    except Exception as ex:
        logging.error('FINAL_UPDATE_R.py - RESPONDED_UPDATE ' + str(ex))
