from google.cloud import pubsub_v1
import os

def get_publisher_client():
    """Returns a Google Cloud Pub/Sub PublisherClient instance."""
    return pubsub_v1.PublisherClient()

def get_subscriber_client():
    """Returns a Google Cloud Pub/Sub SubscriberClient instance."""
    return pubsub_v1.SubscriberClient()

def get_topic_path(project_id: str, topic_id: str) -> str:
    """Returns the full topic path for a given project and topic ID."""
    publisher = get_publisher_client()
    return publisher.topic_path(project_id, topic_id)

def get_subscription_path(project_id: str, subscription_id: str) -> str:
    """Returns the full subscription path for a given project and subscription ID."""
    subscriber = get_subscriber_client()
    return subscriber.subscription_path(project_id, subscription_id)
