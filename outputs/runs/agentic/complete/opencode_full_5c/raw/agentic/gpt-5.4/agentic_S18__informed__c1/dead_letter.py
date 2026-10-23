from __future__ import annotations

from typing import Any

from messaging_client import send_to_queue
from messaging_models import normalize_payload, utc_now_iso


def dead_letter_message(
    dead_letter_queue_url: str,
    failed_payload: dict[str, Any] | str,
    reason: str,
    source_message_id: str | None = None,
) -> dict[str, Any]:
    payload = normalize_payload(failed_payload)
    envelope = {
        "failed_at": utc_now_iso(),
        "reason": reason,
        "source_message_id": source_message_id,
        "payload": payload,
    }
    response = send_to_queue(
        queue_url=dead_letter_queue_url,
        payload=envelope,
        attributes={"dlq_reason": reason},
    )
    return {
        "provider": "aws_sqs",
        "dead_letter_queue_url": dead_letter_queue_url,
        "message_id": response.get("MessageId"),
        "md5_of_body": response.get("MD5OfMessageBody"),
    }
