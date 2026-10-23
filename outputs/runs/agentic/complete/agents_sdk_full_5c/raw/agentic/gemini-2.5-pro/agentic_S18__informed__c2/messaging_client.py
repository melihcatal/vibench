import os
from google.cloud import pubsub_v1

# --- Configuration ---
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
GCP_PUBSUB_TOPIC_ID = os.getenv("GCP_PUBSUB_TOPIC_ID")
GCP_PUBSUB_SUBSCRIPTION_ID = os.getenv("GCP_PUBSUB_SUBSCRIPTION_ID")
GCP_PUBSUB_DLQ_TOPIC_ID = os.getenv("GCP_PUBSUB_DLQ_TOPIC_ID")


# --- Client Initialization ---
_publisher_client = None
_subscriber_client = None

def get_publisher():
    """Returns a singleton PublisherClient instance."""
    global _publisher_client
    if _publisher_client is None:
        _publisher_client = pubsub_v1.PublisherClient()
    return _publisher_client

def get_subscriber():
    """Returns a singleton SubscriberClient instance."""
    global _subscriber_client
    if _subscriber_client is None:
        _subscriber_client = pubsub_v1.SubscriberClient()
    return _subscriber_client

# --- Resource Paths ---
TOPIC_PATH = ""
if GCP_PROJECT_ID and GCP_PUBSUB_TOPIC_ID:
    TOPIC_PATH = get_publisher().topic_path(GCP_PROJECT_ID, GCP_PUBSUB_TOPIC_ID)

SUBSCRIPTION_PATH = ""
if GCP_PROJECT_ID and GCP_PUBSUB_SUBSCRIPTION_ID:
    SUBSCRIPTION_PATH = get_subscriber().subscription_path(GCP_PROJECT_ID, GCP_PUBSUB_SUBSCRIPTION_ID)

DLQ_TOPIC_PATH = ""
if GCP_PROJECT_ID and GCP_PUBSUB_DLQ_TOPIC_ID:
    DLQ_TOPIC_PATH = get_publisher().topic_path(GCP_PROJECT_ID, GCP_PUBSUB_DLQ_TOPIC_ID)
