from __future__ import annotations

from messaging_client import dead_letter_topic_path, get_pubsub_publisher
from messaging_models import MessageRequest, PublishResult


def send_to_dead_letter(
    payload: dict | str,
    attributes: dict | None = None,
    failure_reason: str | None = None,
) -> PublishResult:
    merged_attributes = dict(attributes or {})
    if failure_reason:
        merged_attributes["failure_reason"] = failure_reason
    merged_attributes["dead_letter"] = True
    request = MessageRequest(payload=payload, attributes=merged_attributes)
    publisher = get_pubsub_publisher()
    future = publisher.publish(
        dead_letter_topic_path(),
        request.as_transport_payload(),
        **request.as_transport_attributes(),
    )
    message_id = future.result()
    return PublishResult(
        provider="google-cloud-pubsub",
        destination=dead_letter_topic_path(),
        message_ids=[message_id],
    )
