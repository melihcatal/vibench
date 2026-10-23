from google.cloud import pubsub_v1
import os
from typing import Optional


class MessagingClient:
    """
    Client helper for Google Cloud Pub/Sub messaging operations.
    """

    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()

    def get_topic_path(self, topic_id: str) -> str:
        """Returns the full topic path for the given topic ID."""
        return self.publisher.topic_path(self.project_id, topic_id)

    def get_subscription_path(self, subscription_id: str) -> str:
        """Returns the full subscription path for the given subscription ID."""
        return self.subscriber.subscription_path(self.project_id, subscription_id)

    def validate_topic_exists(self, topic_id: str) -> bool:
        """Validates if a topic exists."""
        topic_path = self.get_topic_path(topic_id)
        try:
            self.publisher.get_topic(request={"topic": topic_path})
            return True
        except Exception:
            return False
