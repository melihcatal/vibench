import os
from google.cloud import pubsub_v1

# Set environment variables
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/service-account-file.json'

# Initialize Pub/Sub client
publisher = pubsub_v1.PublisherClient()
dead_letter_topic_path = publisher.topic_path('my-project-id', 'my-dead-letter-topic')

# Publish a message to dead letter topic
data = 'Failed message'.encode('utf-8')
publisher.publish(dead_letter_topic_path, data=data)