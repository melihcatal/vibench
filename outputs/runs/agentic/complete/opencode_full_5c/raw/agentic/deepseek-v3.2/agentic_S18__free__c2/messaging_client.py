import os
from typing import Dict, Any, Optional
from google.cloud import pubsub_v1
from google.auth import default


class PubSubClient:
    """Google Cloud Pub/Sub client helper with configuration management."""

    def __init__(self, project_id: Optional[str] = None):
        self.project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            _, self.project_id = default()

        self.publisher = None
        self.subscriber = None

    def get_publisher(self) -> pubsub_v1.PublisherClient:
        """Get or create a publisher client."""
        if self.publisher is None:
            self.publisher = pubsub_v1.PublisherClient()
        return self.publisher

    def get_subscriber(self) -> pubsub_v1.SubscriberClient:
        """Get or create a subscriber client."""
        if self.subscriber is None:
            self.subscriber = pubsub_v1.SubscriberClient()
        return self.subscriber

    def get_topic_path(self, topic_id: str) -> str:
        """Get the full topic path."""
        publisher = self.get_publisher()
        return publisher.topic_path(self.project_id, topic_id)

    def get_subscription_path(self, subscription_id: str) -> str:
        """Get the full subscription path."""
        subscriber = self.get_subscriber()
        return subscriber.subscription_path(self.project_id, subscription_id)

    @staticmethod
    def load_config() -> Dict[str, str]:
        """Load Pub/Sub configuration from environment variables."""
        return {
            "project_id": os.environ.get("GOOGLE_CLOUD_PROJECT", ""),
            "topic_id": os.environ.get("PUBSUB_TOPIC_ID", "customer-events"),
            "subscription_id": os.environ.get(
                "PUBSUB_SUBSCRIPTION_ID", "customer-events-sub"
            ),
            "dead_letter_topic_id": os.environ.get(
                "DEAD_LETTER_TOPIC_ID", "dead-letter-events"
            ),
            "region": os.environ.get("PUBSUB_REGION", "us-central1"),
        }

    @staticmethod
    def validate_message_data(data: Dict[str, Any]) -> bool:
        """Validate message data structure."""
        required_fields = ["event_type", "timestamp"]
        for field in required_fields:
            if field not in data:
                return False
        return True

    @staticmethod
    def format_error_message(
        original_data: Dict[str, Any], error: Exception
    ) -> Dict[str, Any]:
        """Format error message for dead letter queue."""
        return {
            "original_message": original_data,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "failed_at": "2024-01-15T10:30:00Z",
        }
