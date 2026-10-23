from __future__ import annotations

import json
from typing import Any, Dict

from google.cloud import pubsub_v1

from messaging_client import dead_letter_topic_path, load_config, publisher_client
from messaging_models import DeadLetterRecord


def send_to_dead_letter(payload: Dict[str, Any], reason: str, project_id: str | None = None) -> str:
    config = load_config(project_id)
    client = publisher_client()
    record = DeadLetterRecord(
        original_message_id=str(payload.get("message_id", "unknown")),
        reason=reason,
        payload=payload,
        attributes={"destination": "pubsub-dlq"},
    )
    future = client.publish(
        dead_letter_topic_path(config),
        json.dumps(record.__dict__, ensure_ascii=False).encode("utf-8"),
        reason=reason,
        original_message_id=record.original_message_id,
    )
    return future.result()
