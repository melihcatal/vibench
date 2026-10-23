from __future__ import annotations

from typing import Any, Dict, Optional

from google.cloud import pubsub_v1

from messaging_client import get_config, get_publisher_client, build_ordering_key
from messaging_models import EventPayload, MessageAttributes, normalize_payload


GOOGLE_PUBSUB_PROVIDER = "google-cloud-pubsub"


def publish_event(payload: Dict[str, Any], attributes: Optional[Dict[str, str]] = None) -> str:
    config = get_config()
    publisher: pubsub_v1.PublisherClient = get_publisher_client()

    normalized = normalize_payload(payload)
    event = EventPayload(
        event_id=str(normalized["event_id"]),
        customer_id=str(normalized["customer_id"]),
        text=str(normalized["text"]),
        status=str(normalized.get("status", "new")),
        created_at=str(normalized.get("created_at") or EventPayload.__dataclass_fields__["created_at"].default_factory()),
        metadata=dict(normalized.get("metadata", {})),
    )
    msg_attrs = MessageAttributes(extra=attributes or {}).as_dict()

    future = publisher.publish(
        config.topic_path,
        event.to_json_bytes(),
        ordering_key=build_ordering_key(event.customer_id),
        **msg_attrs,
    )
    return future.result()
