from google.cloud import pubsub_v1
import os

def get_publisher_client():
    """Gets a Google Cloud Pub/Sub PublisherClient."""
    return pubsub_v1.PublisherClient()

def get_subscriber_client():
    """Gets a Google Cloud Pub/Sub SubscriberClient."""
    return pubsub_v1.SubscriberClient()

def get_project_id():
    """Gets the Google Cloud project ID from environment variables."""
    return os.environ.get("GOOGLE_CLOUD_PROJECT")

def get_topic_path(project_id: str, topic_id: str):
    """Gets the full topic path."""
    return pubsub_v1.PublisherClient.topic_path(project_id, topic_id)

def get_subscription_path(project_id: str, subscription_id: str):
    """Gets the full subscription path."""
    return pubsub_v1.SubscriberClient.subscription_path(project_id, subscription_id)
