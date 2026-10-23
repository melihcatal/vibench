from __future__ import annotations

from typing import Any, Dict, Optional

from messaging_client import get_dead_letter_topic_path, get_publisher_client
from messaging_models import MessagePayload, MessageResult, normalize_json_payload


def send_to_dead_letter(
    payload: Dict[str, Any] | str,
    reason: str,
    original_message_id: Optional[str] = None,
    dead_letter_topic: Optional[str] = None,
) -> MessageResult:
    publisher = get_publisher_client()
    topic_path = get_dead_letter_topic_path(dead_letter_topic)
    normalized = normalize_json_payload(payload)
    attributes = {"failure_reason": reason}
    if original_message_id:
        attributes["original_message_id"] = original_message_id
    message = MessagePayload(body=normalized, attributes=attributes)
    future = publisher.publish(topic_path, message.to_json_bytes(), **attributes)
    published_id = future.result()
    return MessageResult(
        provider="google-cloud-pubsub",
        destination=topic_path,
        message_ids=[published_id],
        status="dead-lettered",
        details={"reason": reason, "original_message_id": original_message_id},
    )
