import os
from google.cloud import logging

client = logging.Client()
logger = client.logger('correlated_logs')

def write_log(log_entry):
    logger.log_struct(log_entry)

if __name__ == '__main__':
    log_entry = {
        'severity': 'INFO',
        'message': 'This is a correlated log entry',
        'component': 'app',
        'operation': 'log_write',
        'correlation_id': '1234567890'
    }
    write_log(log_entry)