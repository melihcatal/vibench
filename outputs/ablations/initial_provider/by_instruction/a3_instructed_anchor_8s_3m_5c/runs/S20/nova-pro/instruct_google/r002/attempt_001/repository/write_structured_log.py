import os
from google.cloud import logging

def write_structured_log(log_name, log_data):
    client = logging.Client()
    logger = client.logger(log_name)
    logger.log_struct(log_data)

if __name__ == '__main__':
    log_name = os.getenv('LOG_NAME', 'my_log')
    log_data = {
        'message': 'This is a structured log event',
        'severity': 'INFO',
        'component': 'app',
        'operation': 'write_log'
    }
    write_structured_log(log_name, log_data)