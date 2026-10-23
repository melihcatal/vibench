import os
from google.cloud import logging

client = logging.Client()
logger = client.logger('structured_logs')

def write_log(log_event):
    entry = logger.entry(log_event)
    entry.resource = client.resource('global')
    client.logging_api.write_entries([entry])

log_event = {'severity': 'INFO','message': 'User logged in', 'user_id': '12345'}
write_log(log_event)