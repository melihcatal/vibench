import os
from google.cloud import logging

client = logging.Client()
logger = client.logger('recent_logs')

filters = [
    'timestamp>="2023-04-01T00:00:00Z"'
]
filter_ = ' AND '.join(filters)
entries = logger.list_entries(filter_=filter_)
for entry in entries:
    print(entry.payload)
