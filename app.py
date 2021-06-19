#App can use docker "config" (simple values) to obtain local syslog server name/port

import logging, logging.handlers, time
from get_docker_secret import get_docker_secret

syslog_host = get_docker_secret('global_syslog_host', default='localhost')
syslog_port = get_docker_secret('global_syslog_port', default='514')

# create logger
logger = logging.getLogger('App-Name')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

sl = logging.handlers.SysLogHandler(address=(syslog_host, syslog_port))

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s\n')

# add formatter to ch
ch.setFormatter(formatter)
sl.setFormatter(formatter)

# add ch to logger
#logger.addHandler(ch)
logger.addHandler(sl)

# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warning('warn message')
logger.error('error message')
logger.critical('critical message')



while True:
	time.sleep(5)
	logger.info('Something Interesting Happened')
