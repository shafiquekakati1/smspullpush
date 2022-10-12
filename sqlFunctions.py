import postgreSQL_vfom
import logging
logging.basicConfig(filename='/tmp/req_res.log', filemode='a',
                    format='%(asctime)s => %(name)s - %(levelname)s - %(message)s')






def INSERT_JOB_DETAILS(ps_connection, generatedID, msisdn, sms, status):
    try:
        cmd = '''
        INSERT INTO "REQ_RES_SMS".job_details (id,msisdn,sms,status)
        VALUES ('{}','{}','{}','{}');
        '''.format(generatedID, msisdn, sms, status)
        postgreSQL_vfom.insert(cmd, ps_connection)
    except Exception as ex:
        logging.error('sqlFunctions.py - INSERT_JOB_DETAILS ' + str(ex))


def INSERT_JOB(ps_connection, generatedID, status):
    try:
        cmd = '''
        INSERT INTO "REQ_RES_SMS".job (id,status)
        VALUES ('{}','{}');
        '''.format(generatedID, status)
        postgreSQL_vfom.insert(cmd, ps_connection)
    except Exception as ex:
        logging.error('sqlFunctions.py - INSERT_JOB ' + str(ex))


def CHECK_READY_SEND(ps_connection):
    try:
        cmd = '''
        SELECT * FROM "REQ_RES_SMS".job j 
        WHERE j.status ='{}'
        LIMIT 1
        '''.format('READY_SEND')
        return postgreSQL_vfom.select(cmd, ps_connection)
    except Exception as ex:
        logging.error('sqlFunctions.py - CHECK_READY_SEND ' + str(ex))


def GET_MSISDN_WHERE_READY(ps_connection, id):
    try:
        cmd = '''
        SELECT * FROM "REQ_RES_SMS".job_details jd
        WHERE jd.id ='{}'
        '''.format(id)
        return postgreSQL_vfom.select(cmd, ps_connection)
    except Exception as ex:
        logging.error('sqlFunctions.py - GET_MSISDN_WHERE_READY ' + str(ex))



def UPDATE_STATUS_IN_JOB(ps_connection, id, status):
    try:
        cmd = '''
        UPDATE "REQ_RES_SMS".job
        SET status='{}'
        WHERE id='{}';
        '''.format(status, id)
        postgreSQL_vfom.update(cmd, ps_connection)
    except Exception as ex:
        logging.error('sqlFunctions.py - UPDATE_STATUS_IN_JOB ' + str(ex))


def UPDATE_STATUS_IN_JOB_DETAILS(ps_connection, id, msisdn, status):
    try:
        cmd = '''
        UPDATE "REQ_RES_SMS".job_details
        SET status='{}'
        WHERE id='{}' AND msisdn='{}';
        '''.format(status, id, msisdn)
        postgreSQL_vfom.update(cmd, ps_connection)
    except Exception as ex:
        logging.error('sqlFunctions.py - UPDATE_STATUS_IN_JOB_DETAILS ' + str(ex))


def UPDATE_SEQ_NUM_IN_JOB_DETAILS(ps_connection, id, msisdn, SEQ_NUM):
    try:
        cmd = '''
        UPDATE "REQ_RES_SMS".job_details
        SET sequence_number='{}'
        WHERE id='{}' AND msisdn='{}';
        '''.format(SEQ_NUM, id, msisdn)
        postgreSQL_vfom.update(cmd, ps_connection)
    except Exception as ex:
        logging.error('sqlFunctions.py - UPDATE_SEQ_NUM_IN_JOB_DETAILS ' + str(ex))


def INSERT_TRANSITION(ps_connection, destination_addr, sequence, source_addr, short_message, receipted_message_id, status):
    try:
        cmd = '''
        INSERT INTO "REQ_RES_SMS".transition (destination_addr,"sequence",source_addr,short_message,receipted_message_id,status)
        VALUES ('{}','{}','{}','{}','{}','{}');
        '''.format(destination_addr, sequence, source_addr, short_message, receipted_message_id, status)
        postgreSQL_vfom.insert(cmd, ps_connection)
    except Exception as ex:
        logging.error('sqlFunctions.py - INSERT_TRANSITION ' + str(ex))


def GET_TRANSITION(ps_connection, status1, status2):
    try:
        cmd = '''
        SELECT * FROM "REQ_RES_SMS".transition T
        WHERE t.status ='{}' 
        OR t.status ='{}'
        OR t.main_status !='DONE'
        '''.format(status1, status2)
        return postgreSQL_vfom.select(cmd, ps_connection)
    except Exception as ex:
        logging.error('sqlFunctions.py - GET_TRANSITION ' + str(ex))


def GET_JOB_DETAILS_TO_UPDATE_SEQUENCE(ps_connection):
    try:
        cmd = '''
        SELECT * FROM "REQ_RES_SMS".job_details jd
        WHERE jd.creation_timestamp::timestamp BETWEEN (now() - interval '1 Day') AND now()
        AND jd.status !='RESPONDED'
        '''
        return postgreSQL_vfom.select(cmd, ps_connection)
    except Exception as ex:
        logging.error('sqlFunctions.py - GET_JOB_DETAILS_TO_UPDATE_SEQUENCE ' + str(ex))


def UPDATE_SEQ_IN_JOB_DETAILS(ps_connection, id, msisdn, SEQ_NUM, status, delivery_status):
    try:
        cmd = '''
        UPDATE "REQ_RES_SMS".job_details
        SET sequence_number='{}' , delivery_status='{}' , status='{}'
        WHERE id='{}' AND msisdn='{}';
        '''.format(SEQ_NUM, delivery_status, status, id, msisdn)
        postgreSQL_vfom.update(cmd, ps_connection)
    except Exception as ex:
        logging.error('sqlFunctions.py - UPDATE_SEQ_IN_JOB_DETAILS ' + str(ex))


def UPDATE_RESPONSE_IN_JOB_DETAILS(ps_connection, id, msisdn, SEQ_NUM, status, response):
    try:
        cmd = '''
        UPDATE "REQ_RES_SMS".job_details
        SET sequence_number='{}' , reponse='{}' , status='{}', response_timestamp=now()
        WHERE id='{}' AND msisdn='{}';
        '''.format(SEQ_NUM, response, status, id, msisdn)
        postgreSQL_vfom.update(cmd, ps_connection)
    except Exception as ex:
        logging.error('sqlFunctions.py - UPDATE_RESPONSE_IN_JOB_DETAILS ' + str(ex))


def UPDATE_JOB_STATUS(ps_connection, id,status):
    try:
        cmd = '''
        UPDATE "REQ_RES_SMS".job
        SET status='{}'
        WHERE id='{}';
        '''.format(status, id)
        postgreSQL_vfom.update(cmd, ps_connection)
    except Exception as ex:
        logging.error('sqlFunctions.py - UPDATE_JOB_STATUS ' + str(ex))


def UPDATE_TRANSITION_STATUS(ps_connection, sequence,status):
    try:
        cmd = '''
        UPDATE "REQ_RES_SMS".transition
        SET main_status='{}'
        WHERE sequence='{}';
        '''.format(status, sequence)
        postgreSQL_vfom.update(cmd, ps_connection)
    except Exception as ex:
        logging.error('sqlFunctions.py - UPDATE_JOB_STATUS ' + str(ex))
