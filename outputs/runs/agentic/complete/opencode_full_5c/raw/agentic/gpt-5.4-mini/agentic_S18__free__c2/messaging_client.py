import json
import os
from typing import Any, Dict, Iterable, List, Optional

from google.cloud import pubsub_v1

from messaging_models import (
    ConsumedMessage,
    MessageBatchItem,
    MessageBatchResult,
    MessageRequest,
    MessageResponse,
    normalize_attributes,
)


def get_project_id() -> str:
    project_id = (
        os.getenv("GOOGLE_CLOUD_PROJECT")
        or os.getenv("GCP_PROJECT")
        or os.getenv("PUBSUB_PROJECT_ID")
    )
    if not project_id:
        raise ValueError("Missing Google Cloud project id")
    return project_id


def publisher_client() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


def subscriber_client() -> pubsub_v1.SubscriberClient:
    return pubsub_v1.SubscriberClient()


def topic_path(topic: str) -> str:
    return publisher_client().topic_path(get_project_id(), topic)


def subscription_path(subscription: str) -> str:
    return subscriber_client().subscription_path(get_project_id(), subscription)


def encode_json_payload(payload: Dict[str, Any]) -> bytes:
    return json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")


def publish_message(request: MessageRequest) -> MessageResponse:
    client = publisher_client()
    topic_name = topic_path(request.topic)
    data = encode_json_payload(request.payload)
    future = client.publish(
        topic_name, data, **normalize_attributes(request.attributes)
    )
    message_id = future.result()
    return MessageResponse(
        provider_message_id=message_id,
        topic=request.topic,
        published_at="",
        attributes=normalize_attributes(request.attributes),
    )


def publish_batch(topic: str, items: Iterable[MessageBatchItem]) -> MessageBatchResult:
    client = publisher_client()
    topic_name = topic_path(topic)
    message_ids: List[str] = []
    for item in items:
        future = client.publish(
            topic_name,
            encode_json_payload(item.data),
            **normalize_attributes(item.attributes),
        )
        message_ids.append(future.result())
    return MessageBatchResult(
        topic=topic,
        provider_batch_id="",
        published_count=len(message_ids),
        message_ids=message_ids,
    )


def consume_one(subscription: str, timeout: float = 5.0) -> Optional[ConsumedMessage]:
    client = subscriber_client()
    response = client.pull(
        request={"subscription": subscription_path(subscription), "max_messages": 1},
        timeout=timeout,
    )
    if not response.received_messages:
        return None
    received = response.received_messages[0]
    payload = json.loads(received.message.data.decode("utf-8") or "{}")
    attrs = dict(received.message.attributes)
    client.acknowledge(
        request={
            "subscription": subscription_path(subscription),
            "ack_ids": [received.ack_id],
        }
    )
    return ConsumedMessage(
        message_id=received.message.message_id,
        payload=payload,
        attributes=attrs,
        subscription=subscription,
    )


def send_dead_letter(
    subscription: str, destination_topic: str, message: ConsumedMessage, reason: str
) -> MessageResponse:
    request = MessageRequest(
        topic=destination_topic,
        payload={
            "failed_message": message.payload,
            "reason": reason,
            "source_subscription": subscription,
        },
        attributes={
            "origin_message_id": message.message_id,
            "source_subscription": subscription,
        },
    )
    return publish_message(request)
