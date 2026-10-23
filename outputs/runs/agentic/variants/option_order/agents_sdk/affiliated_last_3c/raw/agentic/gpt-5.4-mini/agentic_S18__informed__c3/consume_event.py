from __future__ import annotations

from messaging_client import load_config, receive_one
from messaging_models import ConsumeResult, normalize_message_payload


def consume_event() -> ConsumeResult:
    config = load_config()
    message = receive_one(config.consume_target, config=config)
    return ConsumeResult(
        message_id=message.get("message_id", ""),
        body=normalize_message_payload(message.get("body", {})),
        delivery_count=message.get("delivery_count", 0),
        provider=config.provider,
        target=config.consume_target,
    )
