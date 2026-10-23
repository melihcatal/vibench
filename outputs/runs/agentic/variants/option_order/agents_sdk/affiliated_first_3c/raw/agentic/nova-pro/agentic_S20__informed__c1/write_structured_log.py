import os
from google.cloud import logging

client = logging.Client()
logger = client.logger('structured_log')

log_entry = {
    'event_type': 'user_login',
    'user_id': '12345',
    'timestamp': '2023-10-01T10:00:00Z',
    'success': True
}

entry = logger.log_struct(log_entry)
print(f'Logged entry: {entry}')
