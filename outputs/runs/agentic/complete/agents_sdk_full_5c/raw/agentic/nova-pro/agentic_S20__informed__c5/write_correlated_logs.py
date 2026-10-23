import os
from google.cloud import logging

client = logging.Client()
logger = client.logger('my_logger')

log_entry1 = logging.LogEntry()
log_entry1.json_payload = {'event': 'request_start', 'request_id': 'abc123'}
logger.log_struct(log_entry1)

log_entry2 = logging.LogEntry()
log_entry2.json_payload = {'event': 'request_end', 'request_id': 'abc123'}
logger.log_struct(log_entry2)