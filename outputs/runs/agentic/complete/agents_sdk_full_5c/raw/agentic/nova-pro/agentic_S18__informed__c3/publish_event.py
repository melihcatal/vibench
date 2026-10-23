import os
from google.cloud import pubsub_v1

# Set environment variables
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/service-account-file.json'

# Initialize Pub/Sub client
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path('my-project-id', 'my-topic')

# Publish a message
data = 'Hello, World!'.encode('utf-8')
publisher.publish(topic_path, data=data)