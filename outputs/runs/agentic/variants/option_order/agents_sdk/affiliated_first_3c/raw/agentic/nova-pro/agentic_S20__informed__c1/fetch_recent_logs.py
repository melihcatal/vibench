import os
from google.cloud import logging

client = logging.Client()
logger = client.logger('recent_logs')

filter_string = 'timestamp>="2023-10-01T00:00:00Z"'
entries = logger.list_entries(filter_=filter_string)

for entry in entries:
    print(f'Recent log: {entry.text}')
