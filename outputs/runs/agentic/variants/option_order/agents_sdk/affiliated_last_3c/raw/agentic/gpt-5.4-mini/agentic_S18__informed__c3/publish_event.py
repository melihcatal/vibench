from __future__ import annotations

from typing import Any, Dict, Optional

from messaging_client import load_config, send_to_queue
from messaging_models import build_envelope, PublishResult, normalize_message_payload


def publish_event(message_id: str, payload: Any, attributes: Optional[Dict[str, Any]] = None, correlation_id: Optional[str] = None) -> PublishResult:
    config = load_config()
    envelope = build_envelope(message_id=message_id, payload=normalize_message_payload(payload), attributes=attributes, correlation_id=correlation_id)
    send_to_queue(config.publish_target, envelope, config=config)
    return PublishResult(message_id=message_id, status="published", provider=config.provider, target=config.publish_target)
