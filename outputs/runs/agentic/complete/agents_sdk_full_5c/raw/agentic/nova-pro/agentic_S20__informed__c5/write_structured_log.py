import os
from google.cloud import logging

client = logging.Client()
logger = client.logger('my_logger')

log_entry = logging.LogEntry()
log_entry.json_payload = {'event': 'user_login', 'user_id': '12345'}
logger.log_struct(log_entry)