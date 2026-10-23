from __future__ import annotations

from typing import Any, Dict

from messaging_client import publish_json, dead_letter_topic_path
from messaging_models import DeadLetterRequest, PublishRequest, normalize_attributes


def send_dead_letter(request: DeadLetterRequest) -> str:
    dlq_attributes = normalize_attributes(request.attributes)
    dlq_attributes.update({"failed_message_id": request.failed_message_id, "reason": request.reason})
    pub = PublishRequest(
        topic=dead_letter_topic_path(request.destination),
        payload={"failed_message_id": request.failed_message_id, "reason": request.reason, "payload": request.payload},
        attributes=dlq_attributes,
    )
    return publish_json(pub)
