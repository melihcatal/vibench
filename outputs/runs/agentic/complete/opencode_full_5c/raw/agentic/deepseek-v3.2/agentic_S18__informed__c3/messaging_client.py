import os
import json
from typing import Optional, Dict, Any
from google.cloud import pubsub_v1


class PubSubClient:
    """Google Cloud Pub/Sub client helper with configuration management."""

    def __init__(self, project_id: Optional[str] = None):
        self.project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError(
                "GOOGLE_CLOUD_PROJECT environment variable must be set or passed as parameter"
            )

        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()

    def get_topic_path(self, topic_name: str) -> str:
        """Get full topic path for a topic name."""
        return self.publisher.topic_path(self.project_id, topic_name)

    def get_subscription_path(self, subscription_name: str) -> str:
        """Get full subscription path for a subscription name."""
        return self.subscriber.subscription_path(self.project_id, subscription_name)

    def create_topic_if_not_exists(self, topic_name: str) -> str:
        """Create a topic if it doesn't exist."""
        topic_path = self.get_topic_path(topic_name)
        try:
            topic = self.publisher.get_topic(request={"topic": topic_path})
            return topic.name
        except Exception:
            topic = self.publisher.create_topic(request={"name": topic_path})
            return topic.name

    def create_subscription_if_not_exists(
        self,
        subscription_name: str,
        topic_name: str,
        dead_letter_topic: Optional[str] = None,
    ) -> str:
        """Create a subscription if it doesn't exist."""
        subscription_path = self.get_subscription_path(subscription_name)
        topic_path = self.get_topic_path(topic_name)

        try:
            subscription = self.subscriber.get_subscription(
                request={"subscription": subscription_path}
            )
            return subscription.name
        except Exception:
            subscription_config = pubsub_v1.types.Subscription(
                name=subscription_path, topic=topic_path
            )

            if dead_letter_topic:
                dead_letter_topic_path = self.get_topic_path(dead_letter_topic)
                subscription_config.dead_letter_policy = (
                    pubsub_v1.types.DeadLetterPolicy(
                        dead_letter_topic=dead_letter_topic_path,
                        max_delivery_attempts=5,
                    )
                )

            subscription = self.subscriber.create_subscription(
                request={"name": subscription_path, "topic": topic_path}
            )
            return subscription.name

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

    def parse_message(self, data: bytes) -> Dict[str, Any]:
        """Parse message data from bytes."""
        try:
            decoded = data.decode("utf-8")
            return json.loads(decoded)
        except (UnicodeDecodeError, json.JSONDecodeError):
            return {"raw_data": data.decode("utf-8", errors="ignore")}
