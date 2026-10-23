from google.cloud import pubsub_v1
import os
from typing import Optional


class MessagingClient:
    """
    A helper class for managing Google Cloud Pub/Sub clients and configurations.
    """

    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()

    def get_topic_path(self, topic_id: str) -> str:
        """
        Returns the full topic path for a given topic ID.

        Args:
            topic_id: The topic ID.

        Returns:
            str: The full topic path.
        """
        return self.publisher.topic_path(self.project_id, topic_id)

    def get_subscription_path(self, subscription_id: str) -> str:
        """
        Returns the full subscription path for a given subscription ID.

        Args:
            subscription_id: The subscription ID.

        Returns:
            str: The full subscription path.
        """
        return self.subscriber.subscription_path(self.project_id, subscription_id)

    @staticmethod
    def load_config_from_env() -> dict:
        """
        Loads Pub/Sub configuration from environment variables.

        Returns:
            dict: Configuration dictionary.
        """
        return {
            "project_id": os.getenv("GOOGLE_CLOUD_PROJECT_ID"),
            "topic_id": os.getenv("GOOGLE_CLOUD_TOPIC_ID"),
            "subscription_id": os.getenv("GOOGLE_CLOUD_SUBSCRIPTION_ID"),
            "dead_letter_topic_id": os.getenv("GOOGLE_CLOUD_DEAD_LETTER_TOPIC_ID"),
        }
