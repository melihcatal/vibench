import os
import json
from typing import Optional, Dict, Any
from google.cloud import pubsub_v1
from google.auth import default


class MessagingClient:
    """Local configuration and client helper utilities for Google Cloud Pub/Sub."""

    def __init__(self, project_id: Optional[str] = None):
        self.project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            _, self.project_id = default()

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

    def get_topic_path(self, topic_id: str) -> str:
        """Get full topic path from topic ID."""
        return self.publisher.topic_path(self.project_id, topic_id)

    def get_subscription_path(self, subscription_id: str) -> str:
        """Get full subscription path from subscription ID."""
        return self.subscriber.subscription_path(self.project_id, subscription_id)

    def create_topic(self, topic_id: str) -> Dict[str, Any]:
        """Create a new topic."""
        topic_path = self.get_topic_path(topic_id)
        topic = self.publisher.create_topic(request={"name": topic_path})

        return {
            "name": topic.name,
            "labels": dict(topic.labels) if topic.labels else {},
            "message_retention_duration": str(topic.message_retention_duration),
            "provider": "google-cloud-pubsub",
        }

    def create_subscription(
        self, topic_id: str, subscription_id: str, ack_deadline_seconds: int = 10
    ) -> Dict[str, Any]:
        """Create a new subscription."""
        topic_path = self.get_topic_path(topic_id)
        subscription_path = self.get_subscription_path(subscription_id)

        subscription = self.subscriber.create_subscription(
            request={
                "name": subscription_path,
                "topic": topic_path,
                "ack_deadline_seconds": ack_deadline_seconds,
            }
        )

        return {
            "name": subscription.name,
            "topic": subscription.topic,
            "ack_deadline_seconds": subscription.ack_deadline_seconds,
            "message_retention_duration": str(subscription.message_retention_duration),
            "provider": "google-cloud-pubsub",
        }

    def list_topics(self) -> list:
        """List all topics in the project."""
        topics = []
        for topic in self.publisher.list_topics(
            request={"project": f"projects/{self.project_id}"}
        ):
            topics.append(
                {
                    "name": topic.name,
                    "labels": dict(topic.labels) if topic.labels else {},
                }
            )
        return topics

    def list_subscriptions(self) -> list:
        """List all subscriptions in the project."""
        subscriptions = []
        for subscription in self.subscriber.list_subscriptions(
            request={"project": f"projects/{self.project_id}"}
        ):
            subscriptions.append(
                {
                    "name": subscription.name,
                    "topic": subscription.topic,
                    "ack_deadline_seconds": subscription.ack_deadline_seconds,
                }
            )
        return subscriptions

    @staticmethod
    def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
        """Load configuration from file or environment."""
        if config_path and os.path.exists(config_path):
            with open(config_path, "r") as f:
                return json.load(f)

        return {
            "project_id": os.environ.get("GOOGLE_CLOUD_PROJECT"),
            "default_topic": os.environ.get("PUBSUB_TOPIC_ID", "default-topic"),
            "default_subscription": os.environ.get(
                "PUBSUB_SUBSCRIPTION_ID", "default-subscription"
            ),
            "dead_letter_topic": os.environ.get(
                "PUBSUB_DEAD_LETTER_TOPIC_ID", "dead-letter-topic"
            ),
            "batch_settings": {
                "max_messages": int(os.environ.get("PUBSUB_BATCH_MAX_MESSAGES", "100")),
                "max_bytes": int(os.environ.get("PUBSUB_BATCH_MAX_BYTES", "1048576")),
                "max_latency": float(os.environ.get("PUBSUB_BATCH_MAX_LATENCY", "1.0")),
            },
        }
