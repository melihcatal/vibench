from __future__ import annotations

from messaging_client import get_pubsub_publisher, pubsub_topic_path
from messaging_models import MessageRequest, PublishResult


def publish_event(
    payload: dict | str, attributes: dict | None = None, ordering_key: str | None = None
) -> PublishResult:
    request = MessageRequest(
        payload=payload, attributes=attributes or {}, ordering_key=ordering_key
    )
    publisher = get_pubsub_publisher()
    future = publisher.publish(
        pubsub_topic_path(),
        request.as_transport_payload(),
        ordering_key=ordering_key or "",
        **request.as_transport_attributes(),
    )
    published_id = future.result()
    return PublishResult(
        provider="google-cloud-pubsub",
        destination=pubsub_topic_path(),
        message_ids=[published_id],
    )
