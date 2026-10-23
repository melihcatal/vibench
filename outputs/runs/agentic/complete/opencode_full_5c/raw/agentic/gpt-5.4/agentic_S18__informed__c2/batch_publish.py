from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional

from messaging_client import PUBSUB_PROVIDER, get_topic_path, publisher_client
from messaging_models import PublishResult, new_message_record, normalize_pubsub_payload


def batch_publish(
    messages: Iterable[Dict[str, Any]],
    common_attributes: Optional[Dict[str, str]] = None,
    topic_path: Optional[str] = None,
) -> PublishResult:
    client = publisher_client()
    futures: List[Any] = []
    for item in messages:
        payload = normalize_pubsub_payload(item.get("payload", item))
        item_attributes = dict(common_attributes or {})
        item_attributes.update(item.get("attributes", {}))
        record = new_message_record(
            payload=payload,
            attributes=item_attributes,
            ordering_key=item.get("ordering_key"),
        )
        futures.append(
            client.publish(
                get_topic_path(topic_path),
                record.to_json_bytes(),
                event_id=record.message_id,
                **record.attributes,
            )
        )
    return PublishResult(
        provider=PUBSUB_PROVIDER,
        destination=get_topic_path(topic_path),
        message_ids=[future.result() for future in futures],
    )
