import os
from google.cloud import logging

client = logging.Client()
logger = client.logger('my_logger')

def write_correlated_log(log_entry, correlation_id):
    log_entry['correlation_id'] = correlation_id
    logger.log_struct(log_entry)

log_entry = {
    'severity': 'INFO',
    'message': 'This is a correlated log entry'
}
correlation_id = '12345'
write_correlated_log(log_entry, correlation_id)