import os
from google.cloud import pubsub_v1

# Set environment variables
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/service-account-file.json'

# Initialize Pub/Sub client
publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()