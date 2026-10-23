"""
Messaging client helper utilities for Google Cloud Pub/Sub.
Provides configuration loading, client initialization, and connection helpers.
"""

import os
from typing import Optional

from google.cloud import pubsub_v1


class PubSubClientHelper:
    """Helper class for Google Cloud Pub/Sub client configuration and utilities."""

    def __init__(self, project_id: Optional[str] = None):
        self.project_id = project_id or os.environ.get("GCP_PROJECT_ID", "default-project")
        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()

    def get_topic_path(self, topic_id: str) -> str:
        """Return the fully qualified topic path for Google Cloud Pub/Sub."""
        return self.publisher.topic_path(self.project_id, topic_id)

    def get_subscription_path(self, subscription_id: str) -> str:
        """Return the fully qualified subscription path."""
        return self.subscriber.subscription_path(self.project_id, subscription_id)

    def get_dead_letter_topic_path(self, topic_id: str) -> str:
        """Return the fully qualified dead-letter topic path."""
        dl_topic_id = f"{topic_id}-dead-letter"
        return self.publisher.topic_path(self.project_id, dl_topic_id)

    def create_topic(self, topic_id: str) -> str:
        """Create a Pub/Sub topic if it doesn't exist."""
        topic_path = self.get_topic_path(topic_id)
        try:
            self.publisher.create_topic(request={"name": topic_path})
        except Exception:
            pass  # Topic may already exist
        return topic_path

    def create_subscription(
        self,
        subscription_id: str,
        topic_id: str,
        dead_letter_topic_id: Optional[str] = None,
        max_delivery_attempts: int = 5,
    ) -> str:
        """Create a Pub/Sub subscription with optional dead-letter configuration."""
        subscription_path = self.get_subscription_path(subscription_id)
        topic_path = self.get_topic_path(topic_id)

        subscription = {
            "name": subscription_path,
            "topic": topic_path,
            "ack_deadline_seconds": 60,
        }

        if dead_letter_topic_id:
            dl_topic_path = self.get_dead_letter_topic_path(dead_letter_topic_id)
            subscription["dead_letter_policy"] = {
                "dead_letter_topic": dl_topic_path,
                "max_delivery_attempts": max_delivery_attempts,
            }

        try:
            self.subscriber.create_subscription(request=subscription)
        except Exception:
            pass  # Subscription may already exist
        return subscription_path

    def publish_message(
        self,
        topic_id: str,
        data: bytes,
        attributes: Optional[dict] = None,
    ) -> str:
        """Publish a message to a Google Cloud Pub/Sub topic."""
        topic_path = self.get_topic_path(topic_id)
        attributes = attributes or {}
        future = self.publisher.publish(topic_path, data=data, **attributes)
        return future.result()

    def pull_message(
        self,
        subscription_id: str,
        max_messages: int = 1,
    ) -> list:
        """Pull messages from a Google Cloud Pub/Sub subscription."""
        subscription_path = self.get_subscription_path(subscription_id)
        response = self.subscriber.pull(
            request={
                "subscription": subscription_path,
                "max_messages": max_messages,
            },
        )
        return response.received_messages

    def acknowledge_message(self, subscription_id: str, ack_id: str) -> None:
        """Acknowledge a message."""
        subscription_path = self.get_subscription_path(subscription_id)
        self.subscriber.acknowledge(
            request={
                "subscription": subscription_path,
                "ack_ids": [ack_id],
            },
        )

    def close(self) -> None:
        """Close publisher and subscriber clients."""
        self.publisher.close()
        self.subscriber.close()
