import sqlFunctions
import pandas as pd
from datetime import datetime, timedelta
import logging
logging.basicConfig(filename='/tmp/req_res.log', filemode='a',
                    format='%(asctime)s => %(name)s - %(levelname)s - %(message)s')

# DELIVERED
def DELIVERED_UPDATE(ps_connection):
    try:
        DELIVRD_DF = sqlFunctions.GET_TRANSITION(ps_connection ,'DELIVRD', 'UNDELIV')

        currentTimeStamp = datetime.now()
        minus24Hours = currentTimeStamp - timedelta(days=1)

        jobDetailsDF = sqlFunctions.GET_JOB_DETAILS_TO_UPDATE_SEQUENCE(ps_connection)

        print(jobDetailsDF)
        for indexD, rowD in jobDetailsDF.iterrows():
            if 'SENT' in rowD[6] or  'RESPONDED'  in rowD[6] :
                print('no work to do D ')
            else:
                print('updated DET' + rowD[2])
                for index, row in DELIVRD_DF.iterrows():
                    print('updated DET' + rowD[2] + '-TRA' + row[2])
                    if row[6] > minus24Hours < currentTimeStamp and rowD[2] == row[2]:
                        print('updated DET' + rowD[2] + '-TRA' + row[2])
                        sqlFunctions.UPDATE_SEQ_IN_JOB_DETAILS(ps_connection, rowD[0], rowD[2], row[1], 'SENT', row[5])
                        sqlFunctions.UPDATE_TRANSITION_STATUS(ps_connection, row[1],'DONE')
    except Exception as ex:
        logging.error('FINAL_UPDATE_D.py - DELIVERED_UPDATE ' + str(ex))
