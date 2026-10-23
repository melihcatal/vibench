import os
from google.cloud import logging

client = logging.Client()

def fetch_recent_logs():
    logger = client.logger('recent_logs')
    filter_ ='resource.type="global" AND timestamp>="2023-01-01T00:00:00Z"'
    entries = logger.list_entries(filter_=filter_, order_by='timestamp desc')
    for entry in entries:
        print(entry.payload)

fetch_recent_logs()