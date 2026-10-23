import os
from google.cloud import logging

client = logging.Client()
logger = client.logger('correlated_logs')

log_entries = [
    {
        'severity': 'INFO',
       'message': 'Request received',
        'correlationId':'req123'
    },
    {
       'severity': 'INFO',
        'message': 'Response sent',
        'correlationId':'req123'
    }
]
for entry in log_entries:
    log_entry = logging.LogEntry(severity=entry['severity'], text=entry['message'], resource=client.resource('global'))
    log_entry.payload = entry
    logger.log(log_entry)
