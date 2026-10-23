import os
from google.cloud import pubsub_v1

# --- Configuration ---
try:
    GOOGLE_CLOUD_PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
    PUB_SUB_TOPIC_ID = os.environ["PUB_SUB_TOPIC_ID"]
    PUB_SUB_SUBSCRIPTION_ID = os.environ["PUB_SUB_SUBSCRIPTION_ID"]
    PUB_SUB_DLQ_TOPIC_ID = os.environ["PUB_SUB_DLQ_TOPIC_ID"]
except KeyError:
    raise RuntimeError("Required Google Cloud environment variables not set.")

# --- Client Instantiation ---
_publisher_client = None
_subscriber_client = None

def get_publisher() -> pubsub_v1.PublisherClient:
    """Returns a singleton PublisherClient instance."""
    global _publisher_client
    if _publisher_client is None:
        _publisher_client = pubsub_v1.PublisherClient()
    return _publisher_client

def get_subscriber() -> pubsub_v1.SubscriberClient:
    """Returns a singleton SubscriberClient instance."""
    global _subscriber_client
    if _subscriber_client is None:
        _subscriber_client = pubsub_v1.SubscriberClient()
    return _subscriber_client

# --- Resource Paths ---
TOPIC_PATH = get_publisher().topic_path(GOOGLE_CLOUD_PROJECT, PUB_SUB_TOPIC_ID)
SUBSCRIPTION_PATH = get_subscriber().subscription_path(GOOGLE_CLOUD_PROJECT, PUB_SUB_SUBSCRIPTION_ID)
DLQ_TOPIC_PATH = get_publisher().topic_path(GOOGLE_CLOUD_PROJECT, PUB_SUB_DLQ_TOPIC_ID)
