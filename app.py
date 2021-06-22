import logging, logging.handlers, time
from get_docker_secret import get_docker_secret

logger = logging.getLogger('App-Name')
logger.setLevel(logging.DEBUG)

syslog_host = get_docker_secret('global_syslog_host', default='localhost')
syslog_port = get_docker_secret('global_syslog_port', default='514', cast_to=int)
hostname = get_docker_secret('hostname', default='hostname')

formatter = logging.Formatter(f'%(asctime)s {hostname}[%(process)d]: %(name)s - %(levelname)s - %(message)s\n')
formatter.default_time_format='%Y-%m-%dT%H:%M:%SZ'
formatter.default_msec_format=None
formatter.converter=time.gmtime
sl = logging.handlers.SysLogHandler(address=(syslog_host, syslog_port))
#sl.ident = 'containerid'
sl.setFormatter(formatter)
logger.addHandler(sl)

while True:
    time.sleep(5)
    logger.info('Something Interesting Happened')
