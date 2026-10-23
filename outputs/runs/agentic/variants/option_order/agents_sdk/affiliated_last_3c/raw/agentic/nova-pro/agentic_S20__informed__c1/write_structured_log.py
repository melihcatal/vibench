import os
from google.cloud import logging

client = logging.Client()
logger = client.logger('my_logger')

def write_log(log_entry):
    logger.log_struct(log_entry)

log_entry = {
    'severity': 'INFO',
    'message': 'This is a structured log entry',
    'component': 'example_component'
}
write_log(log_entry)