import os
from google.cloud import pubsub_v1

# Helper to instantiate Pub/Sub publisher or subscriber client based on env var

def get_publisher_client():
    """Return a Google Pub/Sub PublisherClient using service account credentials."""
    # GOOGLE_APPLICATION_CREDENTIALS env var should point to JSON key file.
    return pubsub_v1.PublisherClient()

def get_subscriber_client():
    """Return a Google Pub/Sub SubscriberClient using service account credentials."""
    return pubsub_v1.SubscriberClient()
