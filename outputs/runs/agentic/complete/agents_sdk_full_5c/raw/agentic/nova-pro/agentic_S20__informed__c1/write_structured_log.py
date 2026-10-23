import os
from google.cloud import logging

client = logging.Client()
logger = client.logger('my-logger')

log_entry = logging.LogEntry()
log_entry.insert({'message': 'Structured log event'})
logger.log_struct(log_entry)