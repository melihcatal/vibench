from google.cloud import pubsub_v1
import os
from typing import Optional


def get_publisher_client() -> pubsub_v1.PublisherClient:
    """
    Returns a configured Google Cloud Pub/Sub PublisherClient.
    """
    return pubsub_v1.PublisherClient()


def get_subscriber_client() -> pubsub_v1.SubscriberClient:
    """
    Returns a configured Google Cloud Pub/Sub SubscriberClient.
    """
    return pubsub_v1.SubscriberClient()


def get_project_id() -> str:
    """
    Returns the Google Cloud project ID from environment variables.
    """
    return os.getenv("GOOGLE_CLOUD_PROJECT")
