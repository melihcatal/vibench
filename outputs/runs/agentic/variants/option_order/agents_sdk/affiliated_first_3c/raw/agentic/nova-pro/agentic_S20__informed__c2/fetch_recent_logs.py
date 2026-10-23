import os
from google.cloud import logging

client = logging.Client()

query_client = client.get_client()

query = 'resource.type="global" AND timestamp>="2023-10-01T00:00:00Z" AND timestamp<="2023-10-02T00:00:00Z"'
entries = query_client.list_log_entries(filter_=query)

for entry in entries:
    print(entry)