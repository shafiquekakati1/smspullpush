import csv
import time
import uuid
import sqlFunctions, _postgreSQL
import logging
logging.basicConfig(filename='/tmp/req_res_log.log', filemode='a',
                    format='%(asctime)s => %(name)s - %(levelname)s - %(message)s')
import psycopg2
from psycopg2 import Error, pool
import warnings
warnings.simplefilter("ignore", UserWarning)


csvFileInput = '/home/cloud-user/IT/REQ_RES_SMS/INPUT/inputList.csv'
englishSMS = '''
Dear Customer, thank you for using Vodafone services

Do you want Autopayment to be enabled for your Vodafone plan ?
Responsed with:
1. Yes
2. No
'''
arabicSMS = '''
عزيزي العميل ، أشكرك على استخدام خدمات فودافون

هل تريد تفعيل الدفع التلقائي لباقة فودافون الخاصة بك؟
تم الرد بـ:
1. نعم
2. لا
'''

# check if the file format is correct "phone number, language"
# Language only arabic or english
# phone number only digits
try:
    if csvFileInput.endswith('.csv'):
        with open(csvFileInput, 'r') as csvFile:
            csvFile = csv.reader(csvFile)
            for row in csvFile:
                if (row[0].strip().isdigit()):
                    if(row[1].strip() == "arabic" or row[1].strip() == "english"):
                        print(csvFileInput + ' Validated')
                        continue
                    else:
                        print(row[1] + ' is not a supported language')
                        logging.error('INSERT.py - ' +
                                      row[1] + ' is not a supported language')
                        # LOG THIS ERROR ^
                        exit()
                else:
                    print(row[0] + ' is not a number')
                    logging.error('INSERT.py - '+row[0] + ' is not a number')
                    # LOG THIS ERROR ^
                    exit()
    else:
        print(csvFileInput + ' is not a supported file')
        logging.error('INSERT.py - '+csvFileInput +
                      '  is not a supported file')
        # LOG THIS ERROR ^
        exit()
except Exception as ex:
    print(csvFileInput + ' is not a supported file')
    logging.error('INSERT.py - '+csvFileInput +
                  ' is not a supported file' + str(ex))
    # LOG THIS ERROR ^
    exit()

# GENERATE A UNIQUE ID
generatedID = str(uuid.uuid4())
print(generatedID + ' has been generated as the job ID')

count = 0

try:
    # Use getconn() to Get Connection from connection pool
    ps_connection = _postgreSQL.getConnection()
    time.sleep(5)
    if (ps_connection):
        print("successfully received connection from connection pool ")
        #PUT CODE HERE USING CONN ^

        # LOOP THROUGH CSV FILE AND INSERT RECORDS TO DB
        with open(csvFileInput, 'r') as csvFile:
            csvFile = csv.reader(csvFile)
            print('Job '+generatedID + ' is Starting')
            for row in csvFile:
                count += 1
                print(count)
                if row[1].strip() == 'arabic':
                    print('For ' + row[0] + ' the language has been set to ' + row[1])
                    print('The Arabic SMS is ' + arabicSMS)
                    # INSERT TO JOB TO DB
                    sqlFunctions.INSERT_JOB_DETAILS(ps_connection,
                        generatedID, row[0], arabicSMS, 'JOB_STARTED')
                elif row[1].strip() == 'english':
                    print('For ' + row[0] + ' the language has been set to ' + row[1])
                    print('The English SMS is ' + englishSMS)
                    sqlFunctions.INSERT_JOB_DETAILS(ps_connection,
                        generatedID, row[0], englishSMS, 'JOB_STARTED')
                else:
                    print('ERROR => LANGUAGE UNDEFINED/UNSUPPORTED FOR\n' + row[0])
                    print('Job '+generatedID + ' has failed')
                    logging.error(
                        'INSERT.py - ERROR => LANGUAGE UNDEFINED/UNSUPPORTED FOR ' + row[0])
                    # LOG THIS ERROR ^
            sqlFunctions.INSERT_JOB(ps_connection, generatedID, 'READY_SEND')
            print('Job '+generatedID + ' has Finished Inserting to DB')





    # Use this method to release the connection object and send back to connection pool
    _postgreSQL.putConnection(ps_connection)
    print("Put away a PostgreSQL connection")
    logging.info('postgreSQL_vfom.py - Put away a PostgreSQL connection ' + str(ps_connection))




except (Exception, psycopg2.DatabaseError) as error:
    print("Error while connecting to PostgreSQL", error)
    logging.error('postgreSQL_vfom.py - Error while connecting to PostgreSQL ' + str(error))



