from __future__ import annotations

import json
from typing import Any, Mapping, Optional

from google.cloud import pubsub_v1

from messaging_client import load_config, publisher_client, topic_path
from messaging_models import PublishResult, build_envelope


def publish_event(message_id: str, payload: Any, attributes: Optional[Mapping[str, Any]] = None) -> PublishResult:
    envelope = build_envelope(message_id=message_id, payload=payload, attributes=attributes)
    topic = topic_path()
    future = publisher_client().publish(topic, envelope.to_json_bytes(), **envelope.attributes)
    message_id_value = future.result()
    return PublishResult(message_id=message_id_value, topic=topic)


if __name__ == "__main__":
    cfg = load_config()
    publish_event("event-1", {"service": "pubsub", "status": "created"}, {"source": "publisher", "topic": cfg.topic_id})
