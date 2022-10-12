import logging
import logging.handlers
import configparser
import psycopg2
from psycopg2 import pool
from psycopg2 import Error

log = logging.getLogger('vreq')
log.setLevel(logging.INFO)
logfile = '/tmp/sha_request.log'
errorfile='/tmp/sha_errors.log'
hand = logging.handlers.TimedRotatingFileHandler(logfile, when='d', interval=1)
hand.setFormatter(logging.Formatter('%(levelname)-8s [%(asctime)s] %(message)s'))
log.addHandler(hand)

def connection():
        config = configparser.ConfigParser()
        config.read('readfile.ini')
        username=config['postgress']['User']
        password=config['postgress']['password']
        hostname=config['postgress']['hostname']
        port=config['postgress']['port']
        database='bulksmssend'
        try:
                postgreSQL_pool = pool.ThreadedConnectionPool(1, 4, user=username,
                                                password=password,
                                                host=hostname,
                                                port=port,
                                                database=database)
                if (postgreSQL_pool):
                        print("Connection pool created successfully")
                        log.info('postgreSQL_vfom.py - Connection pool created successfully ' + str(postgreSQL_pool))

        except Exception as err:
                log.error('DB Connection Error: {}'.format(err))
                exit()
        return postgreSQL_pool

def connection_check(postgreSQL_pool):
        try:
                ps_connection = postgreSQL_pool.getconn()
        except (Exception, psycopg2.DatabaseError) as error:
                log.error('DB Connection Error: '+str(error))
                return "failure"
        return ps_connection
def release_connection(postgreSQL_pool,ps_connection):
	try:
		ps_connection=postgreSQL_pool.putconn(ps_connection)
	except (Exception, psycopg2.DatabaseError) as error:
		log.error('DB Connection Error: '+str(error))
		return "failure"
	return ps_connection	

