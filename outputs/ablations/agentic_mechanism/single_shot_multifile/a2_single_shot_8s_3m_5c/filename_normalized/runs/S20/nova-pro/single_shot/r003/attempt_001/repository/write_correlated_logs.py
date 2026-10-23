import os
from google.cloud import logging

client = logging.Client()
logger = client.logger('correlated_logs')

def write_correlated_log(log_event, correlation_id):
    log_event['correlation_id'] = correlation_id
    entry = logger.entry(log_event)
    entry.resource = client.resource('global')
    client.logging_api.write_entries([entry])

log_event = {'severity': 'INFO','message': 'Processing request'}
correlation_id = 'abc123'
write_correlated_log(log_event, correlation_id)