import os
from google.cloud import logging

client = logging.Client()
logger = client.logger('my_logger')

query = 'severity=ERROR'
entries = logger.list_entries(filter_=query)
for entry in entries:
    print(entry.text)