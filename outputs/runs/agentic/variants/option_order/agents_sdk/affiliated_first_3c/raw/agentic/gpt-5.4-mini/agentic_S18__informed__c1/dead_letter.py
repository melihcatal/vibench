from __future__ import annotations

from typing import Any, Dict
import json

from messaging_client import get_client, load_config, build_message
from messaging_models import MessageEnvelope, PublishResult


def send_dead_letter(payload: Dict[str, Any], reason: str) -> PublishResult:
    config = load_config()
    envelope = MessageEnvelope.from_mapping(payload)
    envelope.attributes["dead_letter_reason"] = reason
    message = build_message(envelope.to_json(), envelope.id, envelope.content_type, **envelope.attributes)
    with get_client() as client:
        sender = client.get_queue_sender(queue_name=config.dead_letter_queue_name)
        with sender:
            sender.send_messages(message)
    return PublishResult(message_id=envelope.id, succeeded=True, detail=reason)


if __name__ == "__main__":
    result = send_dead_letter({"type": "failed.processing", "body": {"error": "invalid schema"}}, "validation_failed")
    print(json.dumps({"message_id": result.message_id, "succeeded": result.succeeded, "detail": result.detail}))
