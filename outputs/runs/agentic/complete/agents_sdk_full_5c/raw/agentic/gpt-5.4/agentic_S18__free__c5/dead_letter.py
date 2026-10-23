from __future__ import annotations

from typing import Any, Dict, Optional

from messaging_client import dead_letter_topic_path, publisher_client
from messaging_models import MessagePayload


def send_to_dead_letter(failed_payload: Dict[str, Any], reason: str, original_message_id: Optional[str] = None) -> Dict[str, str]:
    dead_letter_body = {
        "failed_payload": failed_payload,
        "reason": reason,
        "original_message_id": original_message_id,
    }
    message = MessagePayload(body=dead_letter_body, attributes={"dead_letter_reason": reason})
    message.ensure_id()
    client = publisher_client()
    future = client.publish(
        dead_letter_topic_path(),
        message.to_json_bytes(),
        **message.attributes,
    )
    published_id = future.result(timeout=30)
    return {"provider": "google-cloud-pubsub", "dead_letter_topic": dead_letter_topic_path(), "message_id": published_id}
