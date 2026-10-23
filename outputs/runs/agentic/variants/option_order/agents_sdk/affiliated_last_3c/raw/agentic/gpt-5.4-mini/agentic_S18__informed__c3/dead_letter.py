from __future__ import annotations

from typing import Any, Dict

from messaging_client import load_config, send_to_queue
from messaging_models import build_envelope, PublishResult, normalize_message_payload


def dead_letter(message_id: str, payload: Any, reason: str, attributes: Dict[str, Any] | None = None) -> PublishResult:
    config = load_config()
    enriched = normalize_message_payload(payload)
    enriched["dead_letter_reason"] = reason
    envelope = build_envelope(message_id=message_id, payload=enriched, attributes=attributes)
    send_to_queue(config.dead_letter_target, envelope, config=config)
    return PublishResult(message_id=message_id, status="dead-lettered", provider=config.provider, target=config.dead_letter_target, details={"reason": reason})
