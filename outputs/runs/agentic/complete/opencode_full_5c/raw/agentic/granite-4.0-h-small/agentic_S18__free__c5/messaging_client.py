# messaging_client.py
"""
Local helper file: messaging_client.py
Provides common configuration loading and client utility functions for Pub/Sub Messaging.
"""

from google.cloud import pubsub_v1
import os


# Provider identifier (GCP Pub/Sub) recognizable from import and client construction
class PubSubConfig:
    """Holds configuration parameters for Google Pub/Sub.

    Attributes:
        project_id (str): GCP project identifier.
        topic_name (str): Name of the topic to publish to.
        subscription_name (str): Name of the subscription to pull from.
    """

    def __init__(self, project_id: str, topic_name: str, subscription_name: str):
        self.project_id = project_id
        self.topic_name = topic_name
        self.subscription_name = subscription_name


def get_pubsub_client() -> pubsub_v1.PublisherClient:
    """Factory that returns a Pub/Sub publisher client.

    Returns:
        pubsub_v1.PublisherClient: Ready-to-use publisher client.
    """
    return pubsub_v1.PublisherClient()


def get_subscriber_client() -> pubsub_v1.SubscriberClient:
    """Factory that returns a Pub/Sub subscriber client.

    Returns:
        pubsub_v1.SubscriberClient: Ready-to-use subscriber client.
    """
    return pubsub_v1.SubscriberClient()
