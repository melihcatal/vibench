import os
import json
from typing import Dict, Any, Optional
from google.cloud import pubsub_v1
from google.auth import default


class MessagingClient:
    """Provide local configuration and client helper utilities for Pub/Sub Messaging."""

    def __init__(self, project_id: Optional[str] = None):
        self.project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            _, self.project_id = default()

        self.publisher_client = None
        self.subscriber_client = None

    def get_publisher(self) -> pubsub_v1.PublisherClient:
        """Get or create a publisher client."""
        if self.publisher_client is None:
            self.publisher_client = pubsub_v1.PublisherClient()
        return self.publisher_client

    def get_subscriber(self) -> pubsub_v1.SubscriberClient:
        """Get or create a subscriber client."""
        if self.subscriber_client is None:
            self.subscriber_client = pubsub_v1.SubscriberClient()
        return self.subscriber_client

    def get_topic_path(self, topic_name: str) -> str:
        """Get full topic path from topic name."""
        return f"projects/{self.project_id}/topics/{topic_name}"

    def get_subscription_path(self, subscription_name: str) -> str:
        """Get full subscription path from subscription name."""
        return f"projects/{self.project_id}/subscriptions/{subscription_name}"

    def create_topic_if_not_exists(self, topic_name: str) -> str:
        """Create topic if it doesn't exist."""
        publisher = self.get_publisher()
        topic_path = self.get_topic_path(topic_name)

        try:
            topic = publisher.get_topic(request={"topic": topic_path})
            return topic_path
        except Exception:
            # Topic doesn't exist, create it
            topic = publisher.create_topic(request={"name": topic_path})
            return topic_path

    def create_subscription_if_not_exists(
        self, subscription_name: str, topic_name: str
    ) -> str:
        """Create subscription if it doesn't exist."""
        subscriber = self.get_subscriber()
        publisher = self.get_publisher()

        subscription_path = self.get_subscription_path(subscription_name)
        topic_path = self.get_topic_path(topic_name)

        try:
            subscription = subscriber.get_subscription(
                request={"subscription": subscription_path}
            )
            return subscription_path
        except Exception:
            # Subscription doesn't exist, create it
            subscription = subscriber.create_subscription(
                request={"name": subscription_path, "topic": topic_path}
            )
            return subscription_path

    def normalize_message(self, data: Any) -> bytes:
        """Normalize message data to bytes."""
        if isinstance(data, dict):
            return json.dumps(data).encode("utf-8")
        elif isinstance(data, str):
            return data.encode("utf-8")
        elif isinstance(data, bytes):
            return data
        else:
            return str(data).encode("utf-8")

    def parse_message(self, data: bytes) -> Any:
        """Parse message data from bytes."""
        try:
            return json.loads(data.decode("utf-8"))
        except json.JSONDecodeError:
            return data.decode("utf-8")

    def get_config(self) -> Dict[str, Any]:
        """Get messaging configuration."""
        return {
            "project_id": self.project_id,
            "default_topic": os.environ.get("PUBSUB_TOPIC", "default-topic"),
            "default_subscription": os.environ.get(
                "PUBSUB_SUBSCRIPTION", "default-subscription"
            ),
            "dead_letter_topic": os.environ.get(
                "PUBSUB_DEAD_LETTER_TOPIC", "dead-letter-topic"
            ),
            "batch_size": int(os.environ.get("PUBSUB_BATCH_SIZE", "100")),
            "max_retry_attempts": int(os.environ.get("PUBSUB_MAX_RETRY_ATTEMPTS", "3")),
        }
