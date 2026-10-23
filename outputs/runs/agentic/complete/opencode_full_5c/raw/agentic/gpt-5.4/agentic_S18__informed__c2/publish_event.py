from __future__ import annotations

from typing import Any, Dict, Optional

from messaging_client import PUBSUB_PROVIDER, get_topic_path, publisher_client
from messaging_models import PublishResult, new_message_record, normalize_pubsub_payload


def publish_event(
    payload: Dict[str, Any],
    attributes: Optional[Dict[str, str]] = None,
    ordering_key: Optional[str] = None,
    topic_path: Optional[str] = None,
) -> PublishResult:
    message = new_message_record(
        normalize_pubsub_payload(payload), attributes, ordering_key
    )
    client = publisher_client()
    future = client.publish(
        get_topic_path(topic_path),
        message.to_json_bytes(),
        event_id=message.message_id,
        **message.attributes,
    )
    message_id = future.result()
    return PublishResult(
        provider=PUBSUB_PROVIDER,
        destination=get_topic_path(topic_path),
        message_ids=[message_id],
    )
