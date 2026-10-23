import os
import json
from typing import Optional, Dict, Any
from google.cloud import pubsub_v1


class PubSubClient:
    """Local configuration and client helper utilities for Google Cloud Pub/Sub."""

    def __init__(
        self,
        project_id: Optional[str] = None,
        topic_id: Optional[str] = None,
        subscription_id: Optional[str] = None,
    ):
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set")

        self.topic_id = topic_id or os.getenv("PUBSUB_TOPIC_ID", "event-topic")
        self.subscription_id = subscription_id or os.getenv(
            "PUBSUB_SUBSCRIPTION_ID", "event-subscription"
        )
        self.dead_letter_topic_id = os.getenv(
            "PUBSUB_DEAD_LETTER_TOPIC_ID", "dead-letter-topic"
        )

        self._publisher = None
        self._subscriber = None

    @property
    def publisher(self):
        """Lazy-loaded publisher client."""
        if self._publisher is None:
            self._publisher = pubsub_v1.PublisherClient()
        return self._publisher

    @property
    def subscriber(self):
        """Lazy-loaded subscriber client."""
        if self._subscriber is None:
            self._subscriber = pubsub_v1.SubscriberClient()
        return self._subscriber

    def get_topic_path(self, topic_id: Optional[str] = None) -> str:
        """Get full topic path."""
        topic = topic_id or self.topic_id
        return self.publisher.topic_path(self.project_id, topic)

    def get_subscription_path(self, subscription_id: Optional[str] = None) -> str:
        """Get full subscription path."""
        subscription = subscription_id or self.subscription_id
        return self.subscriber.subscription_path(self.project_id, subscription)

    def get_dead_letter_topic_path(self) -> str:
        """Get dead letter topic path."""
        return self.publisher.topic_path(self.project_id, self.dead_letter_topic_id)

    def encode_message(self, data: Any) -> bytes:
        """Encode message data to bytes."""
        if isinstance(data, dict):
            return json.dumps(data).encode("utf-8")
        return str(data).encode("utf-8")

    def decode_message(self, data: bytes) -> Any:
        """Decode message data from bytes."""
        try:
            return json.loads(data.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return data.decode("utf-8", errors="ignore")

    def create_event_payload(
        self,
        event_type: str,
        data: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Create standardized event payload."""
        import uuid
        import time

        payload = {
            "event_id": str(uuid.uuid4()),
            "event_type": event_type,
            "timestamp": time.time(),
            "data": data,
            "source": "pubsub_messaging",
        }

        if metadata:
            payload["metadata"] = metadata

        return payload
