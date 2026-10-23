from __future__ import annotations

from typing import Any, Dict, Optional

from messaging_client import (
    PUBSUB_PROVIDER,
    get_dead_letter_topic_path,
    publisher_client,
)
from messaging_models import DeadLetterResult, normalize_pubsub_payload


def send_to_dead_letter(
    source_message_id: str,
    payload: Dict[str, Any],
    reason: str,
    attributes: Optional[Dict[str, str]] = None,
    dead_letter_topic_path: Optional[str] = None,
) -> DeadLetterResult:
    client = publisher_client()
    merged_attributes = {
        "source_message_id": source_message_id,
        "dead_letter_reason": reason,
        **(attributes or {}),
    }
    future = client.publish(
        get_dead_letter_topic_path(dead_letter_topic_path),
        __import__("json")
        .dumps(
            normalize_pubsub_payload(payload), separators=(",", ":"), ensure_ascii=False
        )
        .encode("utf-8"),
        **merged_attributes,
    )
    dead_letter_message_id = future.result()
    return DeadLetterResult(
        provider=PUBSUB_PROVIDER,
        destination=get_dead_letter_topic_path(dead_letter_topic_path),
        dead_letter_message_id=dead_letter_message_id,
        source_message_id=source_message_id,
    )
