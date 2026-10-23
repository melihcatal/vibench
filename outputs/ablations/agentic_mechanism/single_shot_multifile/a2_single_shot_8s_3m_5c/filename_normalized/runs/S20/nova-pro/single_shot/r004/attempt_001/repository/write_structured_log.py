import os
from google.cloud import logging

client = logging.Client()
logger = client.logger('structured_logs')

log_entry = {
    'severity': 'INFO',
   'message': 'User login successful',
    'userId': 'user123',
    'eventTime': '2023-04-01T12:00:00Z'
}
entry = logging.LogEntry(severity=log_entry['severity'], text=log_entry['message'], resource=client.resource('global'))
entry.payload = log_entry
logger.log(entry)
