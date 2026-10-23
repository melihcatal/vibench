import os
from google.cloud import pubsub_v1

def get_publisher_client() -> pubsub_v1.PublisherClient:
    """Returns a configured Google Cloud Pub/Sub PublisherClient."""
    # Google Cloud Pub/Sub client automatically uses GOOGLE_APPLICATION_CREDENTIALS
    # and GOOGLE_CLOUD_PROJECT environment variables for configuration.
    return pubsub_v1.PublisherClient()

def get_subscriber_client() -> pubsub_v1.SubscriberClient:
    """Returns a configured Google Cloud Pub/Sub SubscriberClient."""
    # Google Cloud Pub/Sub client automatically uses GOOGLE_APPLICATION_CREDENTIALS
    # and GOOGLE_CLOUD_PROJECT environment variables for configuration.
    return pubsub_v1.SubscriberClient()
