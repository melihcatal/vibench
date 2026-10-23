import os
from google.cloud import pubsub_v1

# Configuration
project_id = os.getenv('GOOGLE_CLOUD_PROJECT')

# Authenticate
publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()

def get_publisher():
    return publisher

def get_subscriber():
    return subscriber