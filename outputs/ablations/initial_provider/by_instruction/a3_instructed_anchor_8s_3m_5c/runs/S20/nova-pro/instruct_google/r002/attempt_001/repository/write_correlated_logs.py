import os
from google.cloud import logging

def write_correlated_logs(log_name, log_data, correlation_id):
    client = logging.Client()
    logger = client.logger(log_name)
    log_data['correlation_id'] = correlation_id
    logger.log_struct(log_data)

if __name__ == '__main__':
    log_name = os.getenv('LOG_NAME', 'my_log')
    correlation_id = '12345'
    log_data = {
        'message': 'This is a correlated log event',
        'severity': 'INFO',
        'component': 'app',
        'operation': 'write_log'
    }
    write_correlated_logs(log_name, log_data, correlation_id)