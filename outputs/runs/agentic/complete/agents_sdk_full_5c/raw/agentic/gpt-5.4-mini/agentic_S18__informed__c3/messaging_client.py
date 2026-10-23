from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from google.cloud import pubsub_v1

DEFAULT_PUBSUB_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "")
DEFAULT_PUBSUB_TOPIC = os.getenv("PUBSUB_TOPIC", "messaging-topic")
DEFAULT_PUBSUB_SUBSCRIPTION = os.getenv("PUBSUB_SUBSCRIPTION", "messaging-subscription")
DEFAULT_PUBSUB_DEAD_LETTER_TOPIC = os.getenv("PUBSUB_DEAD_LETTER_TOPIC", "messaging-dead-letter")


@dataclass(frozen=True)
class PubSubSettings:
    project_id: str = DEFAULT_PUBSUB_PROJECT
    topic_id: str = DEFAULT_PUBSUB_TOPIC
    subscription_id: str = DEFAULT_PUBSUB_SUBSCRIPTION
    dead_letter_topic_id: str = DEFAULT_PUBSUB_DEAD_LETTER_TOPIC

    @classmethod
    def from_env(cls) -> "PubSubSettings":
        return cls(
            project_id=os.getenv("GOOGLE_CLOUD_PROJECT", DEFAULT_PUBSUB_PROJECT),
            topic_id=os.getenv("PUBSUB_TOPIC", DEFAULT_PUBSUB_TOPIC),
            subscription_id=os.getenv("PUBSUB_SUBSCRIPTION", DEFAULT_PUBSUB_SUBSCRIPTION),
            dead_letter_topic_id=os.getenv("PUBSUB_DEAD_LETTER_TOPIC", DEFAULT_PUBSUB_DEAD_LETTER_TOPIC),
        )


def get_pubsub_settings() -> PubSubSettings:
    return PubSubSettings.from_env()


def publisher_client() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


def subscriber_client() -> pubsub_v1.SubscriberClient:
    return pubsub_v1.SubscriberClient()


def topic_path(project_id: str, topic_id: str) -> str:
    return publisher_client().topic_path(project_id, topic_id)


def subscription_path(project_id: str, subscription_id: str) -> str:
    return subscriber_client().subscription_path(project_id, subscription_id)


def serialize_json(payload: Dict[str, Any]) -> bytes:
    return json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")


def decode_message_data(data: bytes) -> Dict[str, Any]:
    if not data:
        return {}
    return json.loads(data.decode("utf-8"))


def publish_json(topic: str, payload: Dict[str, Any], attributes: Optional[Dict[str, str]] = None) -> str:
    publisher = publisher_client()
    future = publisher.publish(topic, serialize_json(payload), **(attributes or {}))
    return future.result()


def publish_bytes(topic: str, data: bytes, attributes: Optional[Dict[str, str]] = None) -> str:
    publisher = publisher_client()
    future = publisher.publish(topic, data, **(attributes or {}))
    return future.result()
