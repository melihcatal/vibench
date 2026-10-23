from __future__ import annotations

from messaging_client import build_sqs_client, load_config, send_dead_letter
from messaging_models import DeadLetterRequest


def dead_letter_message(message_id: str, reason: str, payload: dict, attributes: dict | None = None) -> dict:
    config = load_config()
    client = build_sqs_client(config)
    request = DeadLetterRequest(
        destination=config.dead_letter_queue_url,
        original_message_id=message_id,
        reason=reason,
        payload=payload,
        attributes=attributes or {},
    )
    return send_dead_letter(client, request)
