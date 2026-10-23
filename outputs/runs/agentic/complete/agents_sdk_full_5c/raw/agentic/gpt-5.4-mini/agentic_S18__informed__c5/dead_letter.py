from __future__ import annotations

from typing import Any, Dict, Optional

from google.cloud import pubsub_v1

from messaging_client import dead_letter_topic_path
from messaging_models import DeadLetterRequest, MessageEnvelope, normalize_attributes, normalize_payload


def send_to_dead_letter(
    payload: Any,
    original_message_id: str,
    reason: str,
    attributes: Optional[Dict[str, Any]] = None,
    project_id: Optional[str] = None,
) -> str:
    request = DeadLetterRequest(
        destination=dead_letter_topic_path(project_id),
        original_message_id=original_message_id,
        reason=reason,
        payload=normalize_payload(payload),
        attributes=normalize_attributes(attributes),
    )
    envelope = MessageEnvelope(
        message_id=request.original_message_id,
        payload={
            "reason": request.reason,
            "original_message_id": request.original_message_id,
            "payload": request.payload,
        },
        attributes=request.attributes,
        source="dead-letter",
    )
    publisher = pubsub_v1.PublisherClient()
    return publisher.publish(request.destination, envelope.to_json().encode("utf-8"), reason=request.reason, **request.attributes).result()
