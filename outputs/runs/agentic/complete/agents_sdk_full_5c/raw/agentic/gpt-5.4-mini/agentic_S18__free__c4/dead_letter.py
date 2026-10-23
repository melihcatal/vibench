import json
from typing import Mapping

from messaging_client import load_config, publisher_client, topic_path
from messaging_models import normalize_attributes


def send_to_dead_letter(payload: Mapping[str, object], reason: str, original_message_id: str) -> str:
    cfg = load_config()
    client = publisher_client()
    dlq_topic = topic_path(cfg.dead_letter_topic_id)
    message = {
        "reason": reason,
        "original_message_id": original_message_id,
        "payload": dict(payload),
    }
    data = json.dumps(message, separators=(",", ":")).encode("utf-8")
    future = client.publish(
        dlq_topic,
        data,
        dead_letter_reason=reason,
        original_message_id=original_message_id,
        **normalize_attributes({"destination": "dead-letter"}),
    )
    return future.result()
