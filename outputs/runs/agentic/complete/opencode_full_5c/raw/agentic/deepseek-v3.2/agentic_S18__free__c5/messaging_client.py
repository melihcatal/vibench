import os
import json
from typing import Dict, Any, Optional
from google.cloud import pubsub_v1


class MessagingClient:
    """Local configuration and client helper utilities for Google Cloud Pub/Sub."""

    def __init__(self, project_id: Optional[str] = None):
        self.project_id = project_id or os.environ.get(
            "GOOGLE_CLOUD_PROJECT", "my-project"
        )
        self.publisher = None
        self.subscriber = None

    def get_publisher(self):
        """Get or create a Pub/Sub publisher client."""
        if self.publisher is None:
            self.publisher = pubsub_v1.PublisherClient()
        return self.publisher

    def get_subscriber(self):
        """Get or create a Pub/Sub subscriber client."""
        if self.subscriber is None:
            self.subscriber = pubsub_v1.SubscriberClient()
        return self.subscriber

    def get_topic_path(self, topic_id: str) -> str:
        """Get full topic path from topic ID."""
        publisher = self.get_publisher()
        return publisher.topic_path(self.project_id, topic_id)

    def get_subscription_path(self, subscription_id: str) -> str:
        """Get full subscription path from subscription ID."""
        subscriber = self.get_subscriber()
        return subscriber.subscription_path(self.project_id, subscription_id)

    @staticmethod
    def load_config() -> Dict[str, Any]:
        """Load messaging configuration from environment."""
        return {
            "project_id": os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project"),
            "topic_id": os.environ.get("PUBSUB_TOPIC_ID", "my-topic"),
            "subscription_id": os.environ.get(
                "PUBSUB_SUBSCRIPTION_ID", "my-subscription"
            ),
            "dead_letter_topic_id": os.environ.get(
                "DEAD_LETTER_TOPIC_ID", "dead-letter-topic"
            ),
            "batch_size": int(os.environ.get("BATCH_SIZE", "100")),
        }

    @staticmethod
    def normalize_payload(payload: Any) -> bytes:
        """Normalize payload to bytes for publishing."""
        if isinstance(payload, dict):
            return json.dumps(payload).encode("utf-8")
        elif isinstance(payload, str):
            return payload.encode("utf-8")
        elif isinstance(payload, bytes):
            return payload
        else:
            return str(payload).encode("utf-8")

    @staticmethod
    def parse_message_data(data: bytes) -> Dict[str, Any]:
        """Parse message data from bytes to dictionary."""
        try:
            return json.loads(data.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return {"raw_data": data.decode("utf-8", errors="ignore")}
