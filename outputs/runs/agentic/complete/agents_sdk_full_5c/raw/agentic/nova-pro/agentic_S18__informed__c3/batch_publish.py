import os
from google.cloud import pubsub_v1

# Set environment variables
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/service-account-file.json'

# Initialize Pub/Sub client
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path('my-project-id', 'my-topic')

# Publish a batch of messages
messages = [
    {'data': 'Message 1'.encode('utf-8')},
    {'data': 'Message 2'.encode('utf-8')}
]
futures = publisher.publish_batch(topic_path, messages)
for future in futures:
    future.result()