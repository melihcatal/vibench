# messaging_client.py
# [HELPER]
# Utilities to obtain authenticated Pub/Sub client objects for Google Cloud.

import os
from google.cloud import pubsub_v1

def get_publisher_client() -> pubsub_v1.PublisherClient:
    """Return a Pub/Sub PublisherClient ready for publishing.
    The client uses Application Default Credentials (GOOGLE_APPLICATION_CREDENTIALS env var)."""
    return pubsub_v1.PublisherClient()

def get_subscriber_client() -> pubsub_v1.SubscriberClient:
    """Return a Pub/Sub SubscriberClient ready for pulling.
    The client uses Application Default Credentials (GOOGLE_APPLICATION_CREDENTIALS env var)."""
    return pubsub_v1.SubscriberClient()
