import os
from google.cloud import logging

client = logging.Client()

query_client = client.get_client()

query = 'severity>=ERROR'
entries = query_client.list_log_entries(filter_=query)

for entry in entries:
    print(entry)