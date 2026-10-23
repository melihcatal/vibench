import os
from google.cloud import pubsub_v1

def get_publisher_client() -> pubsub_v1.PublisherClient:
    """
    Creates and returns a Google Cloud Pub/Sub PublisherClient.
    """
    return pubsub_v1.PublisherClient()

def get_subscriber_client() -> pubsub_v1.SubscriberClient:
    """
    Creates and returns a Google Cloud Pub/Sub SubscriberClient.
    """
    return pubsub_v1.SubscriberClient()

def get_project_id() -> str:
    """
    Retrieves the Google Cloud project ID from environment variables.
    """
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
    return project_id

def get_topic_path(topic_id: str) -> str:
    """
    Constructs the full topic path for a given topic ID.
    """
    project_id = get_project_id()
    return f"projects/{project_id}/topics/{topic_id}"

def get_subscription_path(subscription_id: str) -> str:
    """
    Constructs the full subscription path for a given subscription ID.
    """
    project_id = get_project_id()
    return f"projects/{project_id}/subscriptions/{subscription_id}"
