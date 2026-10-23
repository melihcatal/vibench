from __future__ import annotations

from typing import Any, Dict, Optional

from messaging_client import publisher_client, topic_path
from messaging_models import MessagePayload


def publish_event(payload: Dict[str, Any], attributes: Optional[Dict[str, str]] = None, ordering_key: Optional[str] = None) -> Dict[str, str]:
    message = MessagePayload(body=payload, attributes=attributes or {}, ordering_key=ordering_key)
    message_id = message.ensure_id()
    client = publisher_client()
    future = client.publish(
        topic_path(),
        message.to_json_bytes(),
        message_id=message_id,
        **message.attributes,
        **({"ordering_key": ordering_key} if ordering_key else {}),
    )
    published_id = future.result(timeout=30)
    return {"provider": "google-cloud-pubsub", "topic": topic_path(), "message_id": published_id}
