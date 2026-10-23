from __future__ import annotations

from typing import Any, Dict, Optional

from messaging_client import get_publisher_client, get_topic_path
from messaging_models import MessagePayload, MessageResult, normalize_json_payload


def publish_event(payload: Dict[str, Any] | str, attributes: Optional[Dict[str, str]] = None, topic: Optional[str] = None) -> MessageResult:
    publisher = get_publisher_client()
    topic_path = get_topic_path(topic)
    normalized = normalize_json_payload(payload)
    message = MessagePayload(body=normalized, attributes=attributes or {})
    future = publisher.publish(topic_path, message.to_json_bytes(), **message.attributes)
    published_id = future.result()
    return MessageResult(
        provider="google-cloud-pubsub",
        destination=topic_path,
        message_ids=[published_id],
        status="published",
        details={"attributes": message.attributes},
    )
