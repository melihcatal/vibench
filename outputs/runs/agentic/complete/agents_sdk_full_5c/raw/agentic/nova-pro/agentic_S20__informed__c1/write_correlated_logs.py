import os
from google.cloud import logging

client = logging.Client()
logger = client.logger('my-logger')

log_entry = logging.LogEntry()
log_entry.insert({'message': 'Correlated log event', 'correlation_id': '12345'})
logger.log_struct(log_entry)