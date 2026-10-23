import os
from google.cloud import logging

client = logging.Client()
logger = client.logger('structured_logs')

def write_log(log_entry):
    logger.log_struct(log_entry)

if __name__ == '__main__':
    log_entry = {
        'severity': 'INFO',
        'message': 'This is a structured log entry',
        'component': 'app',
        'operation': 'log_write'
    }
    write_log(log_entry)