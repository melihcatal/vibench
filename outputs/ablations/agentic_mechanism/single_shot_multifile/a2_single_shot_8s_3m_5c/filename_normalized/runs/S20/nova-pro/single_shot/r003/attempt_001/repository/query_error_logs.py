import os
from google.cloud import logging

client = logging.Client()

def query_error_logs():
    logger = client.logger('error_logs')
    filter_ = 'severity>=ERROR'
    entries = logger.list_entries(filter_=filter_, order_by='timestamp desc')
    for entry in entries:
        print(entry.payload)

query_error_logs()