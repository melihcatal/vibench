import os
from google.cloud import logging

client = logging.Client()
logger = client.logger('my_logger')

query_client = client.logging_query_client()
query = 'severity>=ERROR'
start_time = '2023-01-01T00:00:00Z'
end_time = '2023-01-02T00:00:00Z'

entries = query_client.entries(logger_names=['my_logger'], filter_=query, order_by='timestamp desc', start_time=start_time, end_time=end_time)
for entry in entries:
    print(entry)