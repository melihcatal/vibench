from google.cloud import pubsub_v1
import os

def get_publisher_client():
    """Returns a Google Cloud Pub/Sub PublisherClient instance."""
    return pubsub_v1.PublisherClient()

def get_subscriber_client():
    """Returns a Google Cloud Pub/Sub SubscriberClient instance."""
    return pubsub_v1.SubscriberClient()

def get_topic_path(project_id: str, topic_id: str) -> str:
    """Returns the full Pub/Sub topic path."""
    return pubsub_v1.PublisherClient().topic_path(project_id, topic_id)

def get_subscription_path(project_id: str, subscription_id: str) -> str:
    """Returns the full Pub/Sub subscription path."""
    return pubsub_v1.SubscriberClient().subscription_path(project_id, subscription_id)
