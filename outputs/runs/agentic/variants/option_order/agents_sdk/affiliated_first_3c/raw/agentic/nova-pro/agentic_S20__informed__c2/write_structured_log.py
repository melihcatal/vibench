import os
from google.cloud import logging

client = logging.Client()
logger = client.logger('my_logger')

log_entry = logging.LogEntry()
log_entry.json_payload = {'event': 'structured_log', 'timestamp': '2023-10-02T15:01:00Z'}
logger.log_struct(log_entry)