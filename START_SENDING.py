# CHECK JOB TABLE FOR STATUS = READY_SEND
import sqlFunctions
import sender
import pandas as pd
import logging
logging.basicConfig(filename='req_res_log.log', filemode='a',
                    format='%(asctime)s => %(name)s - %(levelname)s - %(message)s')



df = sqlFunctions.CHECK_READY_SEND()

id = df.loc[0][0]
status = df.loc[0][1]
creation_timestamp = df.loc[0][2]
finished_timestamp = df.loc[0][3]

#API WILL CHECK THE JOB, PICK UP THE JOBS, SEND FOR EACH ENTRY IN JOB DETAILS,
def SEND_SMS(msisdn, sms):
    SEQ_NUM = 0
    print('SENDING ' + sms + ' TO ' + msisdn)
    return SEQ_NUM


try:
  if 'READY_SEND' in status:
      print('Ready to send SMSs for Job ID : ' + id)
      dfMSISDN = sqlFunctions.GET_MSISDN_WHERE_READY(id)
      print(dfMSISDN)
      sqlFunctions.UPDATE_STATUS_IN_JOB(id, 'SENDING')
      for index, row in dfMSISDN.iterrows():
          print(row[2], row[3])
          #SEND SMS       
          #AND UPDATES THE STATUS STARTED SENDING, 
          #  FOR EACH MSISDN WILL BE UPDATED WITH SEQ NUMBER
          sqlFunctions.UPDATE_STATUS_IN_JOB_DETAILS(id, row[2], 'STARTED_SENDING')
          print('\n\n')
          sqlFunctions.UPDATE_SEQ_NUM_IN_JOB_DETAILS(id, row[2], sender.start_sending(row[3].encode("utf-8"), row[2]))
          sqlFunctions.UPDATE_JOB_STATUS(id,'DONE')
except Exception as ex:       
    logging.error('START_SENDING.py - ' + str(ex))
       
        



# RESPONSE WILL
