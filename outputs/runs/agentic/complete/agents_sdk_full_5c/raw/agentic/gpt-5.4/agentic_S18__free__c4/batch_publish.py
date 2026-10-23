from __future__ import annotations

from typing import Any, Dict, Iterable, List

from google.cloud import pubsub_v1

from messaging_client import build_ordering_key, get_config, get_publisher_client
from messaging_models import EventPayload, MessageAttributes, normalize_payload


GOOGLE_PUBSUB_PROVIDER = "google-cloud-pubsub"


def publish_batch(payloads: Iterable[Dict[str, Any]]) -> List[str]:
    config = get_config()
    publisher: pubsub_v1.PublisherClient = get_publisher_client()

    futures = []
    for index, payload in enumerate(payloads):
        normalized = normalize_payload(payload)
        event = EventPayload(
            event_id=str(normalized["event_id"]),
            customer_id=str(normalized["customer_id"]),
            text=str(normalized["text"]),
            status=str(normalized.get("status", "new")),
            created_at=str(normalized.get("created_at") or EventPayload.__dataclass_fields__["created_at"].default_factory()),
            metadata=dict(normalized.get("metadata", {})),
        )
        attrs = MessageAttributes(extra={"batch_index": str(index), "event_id": event.event_id}).as_dict()
        futures.append(
            publisher.publish(
                config.topic_path,
                event.to_json_bytes(),
                ordering_key=build_ordering_key(event.customer_id),
                **attrs,
            )
        )

    return [future.result() for future in futures]
