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

#logging.basicConfig(level='DEBUG')

log = logging.getLogger('vreq')
log.setLevel(logging.INFO)
logfile = '/tmp/sha_request.log'
hand = logging.handlers.TimedRotatingFileHandler(logfile, when='d', interval=1)
hand.setFormatter(logging.Formatter('%(levelname)-8s [%(asctime)s] %(message)s'))
log.addHandler(hand)

# Handle delivery receipts (and any MO SMS)
def handle_deliver_sm(pdu):
	try:
		outdict={}
		outdict={'destination_addr':pdu.destination_addr.decode("utf-8"),'sequence':pdu._sequence,'source_addr':pdu.source_addr.decode("utf-8"),'short_message':pdu.short_message.decode("utf-8")}
		text=pdu.short_message.decode("utf-8") 
		if pdu.receipted_message_id is not None:
			start = text.find('stat') + 5
			end = text.find('err', start)-1
			sha=text[start:end]
			outdict.update({'receipted_message_id':pdu.receipted_message_id.decode("utf-8"),'status':sha})
		else:
			outdict.update({'receipted_message_id':None,'status':'response'})
	except Exception as err:
		log.error('Data reciving error: {}'.format(err))
		log.error(pformat(vars(pdu)))
		return 0
	return 0 # cmd status for deliver_sm_resp

def connect():
	(ip, port, sysId, passwd, sys_type) = ("10.14.12.197", "8080", "PDS_testusr", "pds321", "ussd")
	try:
		client = smpplib.client.Client(ip, port)
		client.connect()   # TCP connection
		client.bind_transmitter(system_id=sysId,password=passwd)   # SMPP connection
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

def send_message(message_final,client,msisdn):
	parts, encoding_flag, msg_type_flag = smpplib.gsm.make_parts(message_final)
	client.set_message_sent_handler(lambda pdu: sys.stdout.write('sent {} {}\n'.format(pdu.sequence, pdu.message_id)))
	client.set_message_received_handler(lambda pdu: sys.stdout.write('delivered {}\n'.format(pdu.receipted_message_id)))
	for part in parts:
		pdu = client.send_message(
        			source_addr_ton=smpplib.consts.SMPP_TON_ALNUM,
        			source_addr_npi=smpplib.consts.SMPP_NPI_UNK,
        			# Make sure it is a byte string, not unicode:
        			source_addr='2424',
        			dest_addr_ton=smpplib.consts.SMPP_TON_INTL,
        			dest_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
        			# Make sure these two params are byte strings, not unicode:
        			destination_addr=msisdn,
        			short_message=part,
        			data_coding=encoding_flag,
        			esm_class=msg_type_flag,
        			registered_delivery=True,
      		)
	return 0

def start_sender():
	log.info('Starting Sender')
	while 1:
		try:
			client = connect()
			if client:
				message_final=""
				messages_file=open("message")
				for message in messages_file:
					message_final += message
				send_message(message_final,client,"96877007689")
				client.unbind()
				client.disconnect()
			time.sleep(20)
		except Exception as err:
			log.error('Error in connection: {}'.format(err.message))
			time.sleep(20)
			return 0
	return 1


def start_sending(message_final,msisdn):
	message_final1=str(message_final,"utf-8")
	try:
		client = connect()
		if client:
			seq_number=send_message(message_final1,client,msisdn)
			client.unbind()
			client.disconnect()
	except Exception as err:
		log.error('Error in connection: {}'.format(err.message))
		time.sleep(2)
		return 0
	return seq_number
