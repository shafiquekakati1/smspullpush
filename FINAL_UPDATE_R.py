import sqlFunctions
import pandas as pd
from datetime import datetime, timedelta
import time
import logging
logging.basicConfig(filename='/tmp/req_res_log.log', filemode='a', format='%(asctime)s => %(name)s - %(levelname)s - %(message)s')

#RESPONDED
def RESPONDED_UPDATE():
    try:
        RES_DF = sqlFunctions.GET_TRANSITION('response','response')

        currentTimeStamp = datetime.now()
        minus24Hours = currentTimeStamp - timedelta(days=1)

        """ print('24 Before Timestamp ' + str(minus24Hours))
        print('Current Timestamp ' + str(currentTimeStamp)) """

        jobDetailsDF = sqlFunctions.GET_JOB_DETAILS_TO_UPDATE_SEQUENCE()

        print(RES_DF)
        for indexD, rowD in jobDetailsDF.iterrows():
            if 'SENT' in rowD[6] and 'DELIVRD' in rowD[8]:
                for index, row in RES_DF.iterrows():
                    if row[6] >  minus24Hours < currentTimeStamp and  rowD[2]==row[2] :
                        sqlFunctions.UPDATE_RESPONSE_IN_JOB_DETAILS(rowD[0], rowD[2], row[1], 'RESPONDED',row[3])     
                        sqlFunctions.UPDATE_TRANSITION_STATUS(row[1],'DONE')                           
            else:
                print('no work to do R ')
    except Exception as ex:
        logging.error('FINAL_UPDATE_R.py - RESPONDED_UPDATE ' + str(ex))
