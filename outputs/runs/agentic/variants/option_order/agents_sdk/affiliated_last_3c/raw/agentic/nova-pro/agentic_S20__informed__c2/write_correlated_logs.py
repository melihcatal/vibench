import os
from google.cloud import logging

client = logging.Client()
logger = client.logger('my_logger')

log_entry = logging.LogEntry()
log_entry.text = 'This is a correlated log event'
log_entry.resource.labels['correlation_id'] = '12345'
logger.log_struct(log_entry)