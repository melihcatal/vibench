import os
from google.cloud import logging

client = logging.Client()
logger = client.logger('correlated_logs')

log_entry_1 = {
    'correlation_id': 'abc123',
    'event_type': 'request_start',
    'timestamp': '2023-10-01T10:00:00Z'
}

log_entry_2 = {
    'correlation_id': 'abc123',
    'event_type': 'request_end',
    'timestamp': '2023-10-01T10:00:05Z'
}

entry_1 = logger.log_struct(log_entry_1)
entry_2 = logger.log_struct(log_entry_2)
print(f'Logged entries: {entry_1}, {entry_2}')
