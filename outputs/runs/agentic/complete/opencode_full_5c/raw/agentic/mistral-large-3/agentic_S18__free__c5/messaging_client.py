from google.cloud import pubsub_v1
import os
from typing import Optional, Dict, Any


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
        Returns the full path for a Pub/Sub topic.

        Args:
            topic_id: The ID of the topic.

        Returns:
            str: The full topic path.
        """
        return self.publisher.topic_path(self.project_id, topic_id)

    def get_subscription_path(self, subscription_id: str) -> str:
        """
        Returns the full path for a Pub/Sub subscription.

        Args:
            subscription_id: The ID of the subscription.

        Returns:
            str: The full subscription path.
        """
        return self.subscriber.subscription_path(self.project_id, subscription_id)

    def normalize_message(self, message_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalizes message data to ensure consistent structure.

        Args:
            message_data: Dictionary containing message data.

        Returns:
            Dict[str, Any]: Normalized message data.
        """
        normalized = {
            "data": message_data.get("data", {}),
            "attributes": message_data.get("attributes", {}),
            "message_id": message_data.get("message_id", ""),
        }
        return normalized
