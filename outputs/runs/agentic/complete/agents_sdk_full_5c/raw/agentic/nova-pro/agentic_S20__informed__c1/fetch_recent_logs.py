import os
from google.cloud import logging

client = logging.Client()

query = client.query(log_name='projects/my-project/logs/my-log')
query.add_filter('timestamp', '>', '2023-01-01T00:00:00Z')

for entry in query.run():
    print(entry.payload)