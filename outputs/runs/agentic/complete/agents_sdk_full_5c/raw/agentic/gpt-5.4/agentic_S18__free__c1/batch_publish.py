from __future__ import annotations

from typing import Any

from messaging_client import build_batch_payloads, publisher_client, topic_path
from messaging_models import MessageAttributes, PubSubEvent, PublishResult


PROVIDER = "google-cloud-pubsub"


def publish_batch(events: list[dict[str, Any]]) -> PublishResult:
    client = publisher_client()
    prepared = [
        PubSubEvent(
            event_id=str(item["event_id"]),
            payload=dict(item.get("payload", {})),
            attributes=MessageAttributes.from_dict(item.get("attributes")),
            ordering_key=item.get("ordering_key"),
        )
        for item in events
    ]
    futures = [
        client.publish(topic_path(), data, **kwargs)
        for data, kwargs in build_batch_payloads(prepared)
    ]
    message_ids = [future.result(timeout=30) for future in futures]
    return PublishResult(provider=PROVIDER, message_ids=message_ids)
