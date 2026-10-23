from google.cloud import logging

client = logging.Client()
log_name = 'structured_log'
logger = client.logger(log_name)

def write_log(event):
    logger.log_struct(event)

event = {
    'severity': 'INFO',
    'message': 'This is a structured log event',
    'component': 'app',
    'operation': 'log_write'
}

write_log(event)