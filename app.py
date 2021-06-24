import logging, logging.handlers, time
from get_docker_secret import get_docker_secret

#This is a DEMO app to prove some points about running in a container. It has faults and inconsistencies.
#When running in a container the ideal is to be ephemeral, ie we can destroy and recreate freely without consequence.
#One major limitation is the file system but that can be avoided in many/most cases.
# exceptions would be a db server or some container you need to use but dont control that uses the file system.

#1. Log directly to syslog (to remove file system dependancies)
#   - I log to file here purely to generate data to prove backups
#2. Store data in a database (to remove file system dependancies)
#3. If the file system cannot be avoided automate backups with frequency apropriate to rate of change of data

logger = logging.getLogger('App-Name')
logger.setLevel(logging.DEBUG)

syslog_host = get_docker_secret('global_syslog_host', default='localhost')
syslog_port = get_docker_secret('global_syslog_port', default='514', cast_to=int)
hostname = get_docker_secret('hostname', default='hostname')

log_formatter = logging.Formatter(f'%(asctime)s {hostname} %(name)s[%(process)d]: %(levelname)s - %(message)s\n')
log_formatter.default_time_format='%Y-%m-%dT%H:%M:%SZ'
log_formatter.default_msec_format=None
log_formatter.converter=time.gmtime

syslog_handler = logging.handlers.SysLogHandler(address=(syslog_host, syslog_port))
syslog_handler.setFormatter(log_formatter)

file_handler = logging.FileHandler('/data/appdata.txt')
file_handler.setFormatter(log_formatter)
file_handler.terminator = ''

logger.addHandler(syslog_handler)
logger.addHandler(file_handler)

while True:
    time.sleep(5)
    logger.info('Something Interesting Happened')
