from __future__ import annotations

import json
from typing import Any, Mapping, Optional

from messaging_client import dead_letter_topic_path, publisher_client
from messaging_models import build_envelope, PublishResult


def send_to_dead_letter(message_id: str, payload: Any, attributes: Optional[Mapping[str, Any]] = None) -> PublishResult:
    envelope = build_envelope(message_id=message_id, payload=payload, attributes=attributes)
    topic = dead_letter_topic_path()
    future = publisher_client().publish(topic, envelope.to_json_bytes(), dead_letter="true", **envelope.attributes)
    return PublishResult(message_id=future.result(), topic=topic)
