"""
Local configuration and client helper utilities for Pub/Sub Messaging.
"""

import os
from typing import Any, Dict, Optional

from google.cloud import pubsub_v1
from google.api_core.exceptions import GoogleAPIError


class MessagingConfig:
    """Configuration loader for Google Cloud Pub/Sub."""

    def __init__(self):
        self.project_id = os.environ.get(
            "GOOGLE_CLOUD_PROJECT", os.environ.get("GOOGLE_CLOUD_PROJECT_ID", "")
        )
        self.topic_id = os.environ.get("PUBSUB_TOPIC_ID", "events-topic")
        self.subscription_id = os.environ.get("PUBSUB_SUBSCRIPTION_ID", "events-subscription")
        self.dead_letter_topic_id = os.environ.get(
            "PUBSUB_DEAD_LETTER_TOPIC_ID", "events-dead-letter-topic"
        )
        self.credentials_path = os.environ.get(
            "GOOGLE_APPLICATION_CREDENTIALS", ""
        )
        self.endpoint = os.environ.get(
            "PUBSUB_EMULATOR_HOST", "pubsub.googleapis.com:443"
        )

    @property
    def topic_path(self) -> str:
        return f"projects/{self.project_id}/topics/{self.topic_id}"

    @property
    def subscription_path(self) -> str:
        return f"projects/{self.project_id}/subscriptions/{self.subscription_id}"

    @property
    def dead_letter_topic_path(self) -> str:
        return f"projects/{self.project_id}/topics/{self.dead_letter_topic_id}"

    def validate(self) -> bool:
        return bool(self.project_id) and bool(self.topic_id)


class PubSubClientHelper:
    """Helper utilities for Google Cloud Pub/Sub client operations."""

    def __init__(self, config: Optional[MessagingConfig] = None):
        self.config = config or MessagingConfig()
        self._publisher: Optional[pubsub_v1.PublisherClient] = None
        self._subscriber: Optional[pubsub_v1.SubscriberClient] = None

    @property
    def publisher(self) -> pubsub_v1.PublisherClient:
        """Get or create the Google Cloud Pub/Sub publisher client."""
        if self._publisher is None:
            publisher_options = pubsub_v1.types.PublisherOptions(
                batch_settings=pubsub_v1.types.BatchSettings(
                    max_bytes=1024 * 1024,
                    max_latency=0.05,
                    max_messages=100,
                )
            )
            self._publisher = pubsub_v1.PublisherClient(
                publisher_options=publisher_options
            )
        return self._publisher

    @property
    def subscriber(self) -> pubsub_v1.SubscriberClient:
        """Get or create the Google Cloud Pub/Sub subscriber client."""
        if self._subscriber is None:
            subscriber_options = pubsub_v1.types.SubscriberOptions(
                flow_control=pubsub_v1.types.FlowControl(max_messages=10)
            )
            self._subscriber = pubsub_v1.SubscriberClient(
                subscriber_options=subscriber_options
            )
        return self._subscriber

    def create_message_data(
        self,
        payload: bytes,
        attributes: Optional[Dict[str, str]] = None,
    ) -> pubsub_v1.types.PubsubMessage:
        """Create a Pub/Sub message with data and attributes."""
        msg_attrs = attributes or {}
        message = pubsub_v1.types.PubsubMessage(data=payload, attributes=msg_attrs)
        return message

    def publish_with_retry(
        self,
        topic_path: str,
        data: bytes,
        attributes: Optional[Dict[str, str]] = None,
        max_retries: int = 3,
    ) -> str:
        """Publish a message with retry logic for transient errors."""
        message = self.create_message_data(data, attributes)
        last_error = None

        for attempt in range(max_retries):
            try:
                future = self.publisher.publish(topic_path, message.data, **message.attributes)
                message_id = future.result(timeout=30)
                return message_id
            except GoogleAPIError as e:
                last_error = e
                continue

        raise last_error or Exception("Failed to publish message after retries")

    def build_dead_letter_policy(
        self,
        dead_letter_topic_path: str,
        max_delivery_attempts: int = 5,
    ) -> pubsub_v1.types.DeadLetterPolicy:
        """Build a dead letter policy configuration."""
        return pubsub_v1.types.DeadLetterPolicy(
            dead_letter_topic=dead_letter_topic_path,
            max_delivery_attempts=max_delivery_attempts,
        )

    def close(self) -> None:
        """Close publisher and subscriber clients."""
        if self._publisher is not None:
            self._publisher.stop()
        if self._subscriber is not None:
            self._subscriber.close()
