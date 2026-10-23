import os
from google.cloud import pubsub_v1

def get_publisher_client():
    """Gets a Google Cloud Pub/Sub publisher client."""
    return pubsub_v1.PublisherClient()

def get_subscriber_client():
    """Gets a Google Cloud Pub/Sub subscriber client."""
    return pubsub_v1.SubscriberClient()

def get_project_id():
    """Gets the Google Cloud Project ID from environment variables."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")
    return project_id

def get_topic_name(topic_id: str):
    """Gets the full topic name."""
    project_id = get_project_id()
    return f"projects/{project_id}/topics/{topic_id}"

def get_subscription_name(subscription_id: str):
    """Gets the full subscription name."""
    project_id = get_project_id()
    return f"projects/{project_id}/subscriptions/{subscription_id}"
