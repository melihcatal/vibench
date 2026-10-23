from __future__ import annotations

import json
import os
from typing import Any

from google.cloud import pubsub_v1

from messaging_models import ConsumedMessage


def get_gcp_project_id() -> str:
    project_id = os.environ.get("GCP_PROJECT_ID") or os.environ.get(
        "GOOGLE_CLOUD_PROJECT"
    )
    if not project_id:
        raise ValueError("Missing GCP_PROJECT_ID or GOOGLE_CLOUD_PROJECT")
    return project_id


def get_topic_id(default: str = "customer-events") -> str:
    return os.environ.get("PUBSUB_TOPIC_ID", default)


def get_subscription_id(default: str = "customer-events-sub") -> str:
    return os.environ.get("PUBSUB_SUBSCRIPTION_ID", default)


def get_dead_letter_topic_id(default: str = "customer-events-dead-letter") -> str:
    return os.environ.get("PUBSUB_DEAD_LETTER_TOPIC_ID", default)


def publisher_client() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


def subscriber_client() -> pubsub_v1.SubscriberClient:
    return pubsub_v1.SubscriberClient()


def topic_path(topic_id: str | None = None) -> str:
    client = publisher_client()
    return client.topic_path(get_gcp_project_id(), topic_id or get_topic_id())


def subscription_path(subscription_id: str | None = None) -> str:
    client = subscriber_client()
    return client.subscription_path(
        get_gcp_project_id(), subscription_id or get_subscription_id()
    )


def dead_letter_topic_path(topic_id: str | None = None) -> str:
    client = publisher_client()
    return client.topic_path(
        get_gcp_project_id(), topic_id or get_dead_letter_topic_id()
    )


def decode_message(
    message: Any, ack_id: str, delivery_attempt: int | None = None
) -> ConsumedMessage:
    data_text = (
        message.data.decode("utf-8")
        if isinstance(message.data, (bytes, bytearray))
        else str(message.data)
    )
    publish_time = None
    if getattr(message, "publish_time", None) is not None:
        publish_time = message.publish_time.isoformat()
    return ConsumedMessage(
        ack_id=ack_id,
        message_id=message.message_id,
        data_text=data_text,
        attributes=dict(message.attributes),
        publish_time=publish_time,
        ordering_key=getattr(message, "ordering_key", None),
        delivery_attempt=delivery_attempt,
    )


def parse_json_text(data_text: str) -> dict[str, Any]:
    return json.loads(data_text)
