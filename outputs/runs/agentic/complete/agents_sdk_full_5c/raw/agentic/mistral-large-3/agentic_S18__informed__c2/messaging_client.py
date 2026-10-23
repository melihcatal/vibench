"""Local configuration and client helper utilities for Pub/Sub Messaging."""
import os
from typing import Optional, Dict, Any
from google.cloud import pubsub_v1
from google.api_core.exceptions import GoogleAPICallError
from messaging_models import Message, normalize_pubsub_message


class PubSubClient:
    """Google Cloud Pub/Sub client helper for publishing and consuming messages."""

    def __init__(self, project_id: Optional[str] = None):
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()

    def publish(self, topic: str, message: Message) -> str:
        """Publish a single message to a Google Cloud Pub/Sub topic."""
        topic_path = self.publisher.topic_path(self.project_id, topic)
        future = self.publisher.publish(
            topic_path,
            data=str(message.body).encode("utf-8"),
            **message.attributes or {}
        )
        return future.result()

    def consume(self, subscription: str, timeout: Optional[float] = None) -> Optional[Message]:
        """Consume a single message from a Google Cloud Pub/Sub subscription."""
        subscription_path = self.subscriber.subscription_path(self.project_id, subscription)
        response = self.subscriber.pull(
            request={
                "subscription": subscription_path,
                "max_messages": 1,
                "return_immediately": False
            },
            timeout=timeout
        )
        if not response.received_messages:
            return None
        received_message = response.received_messages[0]
        message = normalize_pubsub_message(received_message.message)
        self.subscriber.acknowledge(
            request={
                "subscription": subscription_path,
                "ack_ids": [received_message.ack_id]
            }
        )
        return message

    def dead_letter(self, dead_letter_topic: str, message: Message) -> str:
        """Send a failed message to a dead-letter topic."""
        return self.publish(dead_letter_topic, message)

    def batch_publish(self, topic: str, messages: list[Message]) -> list[str]: 
        """Publish a batch of messages to a Google Cloud Pub/Sub topic."""
        topic_path = self.publisher.topic_path(self.project_id, topic)
        futures = []
        for message in messages:
            future = self.publisher.publish(
                topic_path,
                data=str(message.body).encode("utf-8"),
                **message.attributes or {}
            )
            futures.append(future)
        return [future.result() for future in futures]