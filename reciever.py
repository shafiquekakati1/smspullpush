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

#logging.basicConfig(level='DEBUG')

log = logging.getLogger('vreq')
log.setLevel(logging.INFO)
logfile = 'sha_request.log'
errorfile='sha_errors.log'
hand = logging.handlers.TimedRotatingFileHandler(logfile, when='d', interval=1)
hand.setFormatter(logging.Formatter('%(levelname)-8s [%(asctime)s] %(message)s'))
log.addHandler(hand)

# Handle delivery receipts (and any MO SMS)
def handle_deliver_sm(pdu):
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
		sqlFunctions.INSERT_TRANSITION(outdict['destination_addr'],outdict['sequence'],outdict['source_addr'],outdict['short_message'],outdict['receipted_message_id'],outdict['status'])
	except Exception as err:
		log.error('Data reciving error: {}'.format(err))
		log.error('Data reciving error: {}'.format(values))
		log.error(pformat(vars(pdu)))
		return 0
	return 0 # cmd status for deliver_sm_resp

def connect():
	(ip, port, sysId, passwd, sys_type) = ("10.14.12.197", "8080", "PDS_testusr", "pds321", "ussd")
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

def start_reciever():
	while 1:
		log.info('Starting Reciever')
		try:
			client = connect()
			if client:
				client.set_message_received_handler(lambda pdu: handle_deliver_sm(pdu))
				client.set_message_sent_handler(lambda pdu: sys.stdout.write('sent {} {}\n'.format(pdu.sequence, pdu.message_id)))
				log.info('Reciever Started')
				client.listen()
		except Exception as err:
			log.error('Error in connection: {}'.format(err.message))
			time.sleep(20)
			continue
#start_reciever()
