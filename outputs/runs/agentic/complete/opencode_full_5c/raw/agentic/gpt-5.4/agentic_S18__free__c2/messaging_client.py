from __future__ import annotations

import base64
import json
import os
from typing import Any

from google.cloud import pubsub_v1

from messaging_models import ConsumedMessage, PublishRequest


PUBSUB_PROJECT_ID_ENV = "GCP_PROJECT_ID"
PUBSUB_TOPIC_ENV = "GCP_PUBSUB_TOPIC"
PUBSUB_SUBSCRIPTION_ENV = "GCP_PUBSUB_SUBSCRIPTION"
PUBSUB_DEAD_LETTER_TOPIC_ENV = "GCP_PUBSUB_DEAD_LETTER_TOPIC"


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def get_project_id() -> str:
    return get_required_env(PUBSUB_PROJECT_ID_ENV)


def get_topic_name() -> str:
    return get_required_env(PUBSUB_TOPIC_ENV)


def get_subscription_name() -> str:
    return get_required_env(PUBSUB_SUBSCRIPTION_ENV)


def get_dead_letter_topic_name() -> str:
    return get_required_env(PUBSUB_DEAD_LETTER_TOPIC_ENV)


def publisher_client() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


def subscriber_client() -> pubsub_v1.SubscriberClient:
    return pubsub_v1.SubscriberClient()


def topic_path(topic_name: str | None = None) -> str:
    client = publisher_client()
    return client.topic_path(get_project_id(), topic_name or get_topic_name())


def subscription_path(subscription_name: str | None = None) -> str:
    client = subscriber_client()
    return client.subscription_path(
        get_project_id(), subscription_name or get_subscription_name()
    )


def publish_request(request: PublishRequest, topic_name: str | None = None) -> str:
    client = publisher_client()
    future = client.publish(
        topic_path(topic_name),
        request.wire_payload(),
        **request.attributes,
        ordering_key=request.ordering_key or "",
    )
    return future.result()


def pull_one(
    subscription_name: str | None = None, auto_ack: bool = False
) -> ConsumedMessage | None:
    client = subscriber_client()
    response = client.pull(
        request={
            "subscription": subscription_path(subscription_name),
            "max_messages": 1,
        }
    )
    if not response.received_messages:
        return None
    received = response.received_messages[0]
    payload = json.loads(received.message.data.decode("utf-8"))
    message = ConsumedMessage(
        ack_id=received.ack_id,
        message_id=received.message.message_id or payload.get("message_id", ""),
        payload=payload,
        attributes=dict(received.message.attributes),
        published_at=payload.get("published_at"),
    )
    if auto_ack:
        ack_message(received.ack_id, subscription_name=subscription_name)
    return message


def ack_message(ack_id: str, subscription_name: str | None = None) -> None:
    client = subscriber_client()
    client.acknowledge(
        request={
            "subscription": subscription_path(subscription_name),
            "ack_ids": [ack_id],
        }
    )


def build_dead_letter_payload(message: ConsumedMessage, reason: str) -> PublishRequest:
    payload = {
        "original_message_id": message.message_id,
        "failed_at": message.published_at,
        "dead_letter_reason": reason,
        "payload": message.payload,
        "attributes": message.attributes,
    }
    attributes = dict(message.attributes)
    attributes["dead_letter_reason"] = reason
    attributes["original_message_id"] = message.message_id
    return PublishRequest.from_input(
        payload=payload, attributes=attributes, message_id=message.message_id
    )


def pubsub_push_envelope(
    payload: dict[str, Any], attributes: dict[str, str] | None = None
) -> dict[str, Any]:
    encoded = base64.b64encode(
        json.dumps(payload, ensure_ascii=False).encode("utf-8")
    ).decode("utf-8")
    return {
        "message": {
            "data": encoded,
            "attributes": attributes or {},
            "messageId": payload.get("message_id", ""),
        }
    }
