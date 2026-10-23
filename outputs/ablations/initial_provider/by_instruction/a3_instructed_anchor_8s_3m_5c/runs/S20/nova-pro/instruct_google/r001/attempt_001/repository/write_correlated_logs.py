from google.cloud import logging
import uuid

client = logging.Client()
log_name = 'correlated_logs'
logger = client.logger(log_name)

def write_log(event, correlation_id):
    event['correlation_id'] = correlation_id
    logger.log_struct(event)

correlation_id = str(uuid.uuid4())
event1 = {
    'severity': 'INFO',
    'message': 'This is a correlated log event 1',
    'component': 'app',
    'operation': 'log_write'
}
event2 = {
    'severity': 'INFO',
    'message': 'This is a correlated log event 2',
    'component': 'app',
    'operation': 'log_write'
}

write_log(event1, correlation_id)
write_log(event2, correlation_id)