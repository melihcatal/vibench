import os
from google.cloud import logging

client = logging.Client()
logger = client.logger('my_logger')

query = 'timestamp>="2023-01-01T00:00:00Z" AND timestamp<="2023-12-31T23:59:59Z"'
entries = logger.list_entries(filter_=query)
for entry in entries:
    print(entry.text)