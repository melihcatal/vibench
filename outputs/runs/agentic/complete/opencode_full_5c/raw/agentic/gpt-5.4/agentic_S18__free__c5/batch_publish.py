from __future__ import annotations

from messaging_client import get_pubsub_publisher, pubsub_topic_path
from messaging_models import MessageRequest, PublishResult


def batch_publish(messages: list[dict]) -> PublishResult:
    publisher = get_pubsub_publisher()
    topic = pubsub_topic_path()
    futures = []
    for item in messages:
        request = MessageRequest(
            payload=item.get("payload", {}),
            attributes=item.get("attributes", {}),
            ordering_key=item.get("ordering_key"),
            message_id=item.get("message_id") or None,
        )
        futures.append(
            publisher.publish(
                topic,
                request.as_transport_payload(),
                ordering_key=request.ordering_key or "",
                **request.as_transport_attributes(),
            )
        )
    return PublishResult(
        provider="google-cloud-pubsub",
        destination=topic,
        message_ids=[future.result() for future in futures],
    )
