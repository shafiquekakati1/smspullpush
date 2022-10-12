#!/bin/python3

import logging
import logging.handlers
import sys
import time
import re
import smpplib.gsm
import smpplib.client
import smpplib.consts
from pprint import pprint,pformat
import sqlFunctions
import threading
import db


#logging.basicConfig(level='DEBUG')

log = logging.getLogger('vreq')
log.setLevel(logging.INFO)
logfile = '/tmp/sha_request.log'
errorfile='/tmp/sha_errors.log'
hand = logging.handlers.TimedRotatingFileHandler(logfile, when='d', interval=1)
hand.setFormatter(logging.Formatter('%(levelname)-8s [%(asctime)s] %(message)s'))
log.addHandler(hand)


# Handle delivery receipts (and any MO SMS)
def handle_deliver_sm(pdu):
	ps_connection=db.connection_check(postgreSQL_pool)
	if ps_connection == "failure" :
		#exit()
		print(ps_connection)
		#thread.exit()
	try:
		values=[]
		outdict={}
		outdict={'destination_addr':pdu.destination_addr.decode("utf-8"),'sequence':pdu._sequence,'source_addr':pdu.source_addr.decode("utf-8"),'short_message':pdu.short_message.decode("utf-8")}
		text=pdu.short_message.decode("utf-8") 
		if pdu.receipted_message_id is not None:
			start = text.find('stat') + 5
			end = text.find('err', start)-1
			sha=text[start:end]
			outdict.update({'receipted_message_id':pdu.receipted_message_id.decode("utf-8"),'status':sha})
		else:
			outdict.update({'receipted_message_id':'None','status':'response'})
		log.info('SMS Recieved: {}'.format(outdict))
		sqlFunctions.INSERT_TRANSITION(ps_connection,outdict['destination_addr'],outdict['sequence'],outdict['source_addr'],outdict['short_message'],outdict['receipted_message_id'],outdict['status'])
		db.release_connection(postgreSQL_pool,ps_connection)
	except Exception as err:
		log.error('Data reciving error: {}'.format(err))
		log.error('Data reciving error: {}'.format(values))
		log.error(pformat(vars(pdu)))
		return 0
	return 0 # cmd status for deliver_sm_resp

def connect(iip,iport):
	(ip, port, sysId, passwd, sys_type) = (iip, iport, "PDS_testusr", "pds321", "ussd")
	try:
		client = smpplib.client.Client(ip, port)
		client.connect()   # TCP connection
		client.bind_transceiver(system_id=sysId,password=passwd)   # SMPP connection
	except smpplib.exceptions.PDUError as pduer:
		log.error('error while trying to connect1: {}'.format(pduer))
		return 0
	except smpplib.exceptions.ConnectionError as coner:
		log.error('error while trying to connect2: {}'.format(coner))
		return 0
	except smpplib.exceptions.UnknownCommandError as unkn:
		log.error('error while trying to connect3: {}'.format(unkn))
		return 0
	return client

def start_reciever1():
	while 1:
		log.info('Starting Reciever1')
		try:
			client1 = connect("10.14.12.197","8080")
			if client1:
				client1.set_message_received_handler(lambda pdu: handle_deliver_sm(pdu))
				client1.set_message_sent_handler(lambda pdu: sys.stdout.write('sent {} {}\n'.format(pdu.sequence, pdu.message_id)))
				log.info('Reciever1 Started')
				client1.listen()
		except Exception as err:
			log.error('Error in connection: {}'.format(err.message))
			time.sleep(20)
			continue

def start_reciever2():
        while 1:
                log.info('Starting Reciever2')
                try:
                        client2 = connect("10.14.12.210","8080")
                        if client2:
                                client2.set_message_received_handler(lambda pdu: handle_deliver_sm(pdu))
                                client2.set_message_sent_handler(lambda pdu: sys.stdout.write('sent {} {}\n'.format(pdu.sequence, pdu.message_id)))
                                log.info('Reciever2 Started')
                                client2.listen()
                except Exception as err:
                        log.error('Error in connection: {}'.format(err.message))
                        time.sleep(20)
                        continue

if __name__ == "__main__":
	postgreSQL_pool = db.connection()
	threads = list()
	x = threading.Thread(target=start_reciever1,daemon=True)	
	threads.append(x)
	x.start()
	x = threading.Thread(target=start_reciever2,daemon=True)
	threads.append(x)
	x.start()
	for index, thread in enumerate(threads):
		thread.join()
