from __future__ import annotations

from typing import Any

from messaging_client import publisher_client, topic_path
from messaging_models import MessageEvent, normalize_attributes


def batch_publish(messages: list[dict[str, Any]]) -> dict[str, Any]:
    client = publisher_client()
    futures: list[tuple[str, Any]] = []
    for item in messages:
        event = MessageEvent(
            payload=item["payload"],
            attributes=normalize_attributes(item.get("attributes")),
            ordering_key=item.get("ordering_key"),
            event_id=str(
                item.get("event_id")
                or item.get("message_id")
                or MessageEvent(payload=item["payload"]).event_id
            ),
        )
        attrs = dict(event.attributes)
        attrs.setdefault("event_id", event.event_id)
        future = client.publish(
            topic_path(),
            event.to_pubsub_payload(),
            ordering_key=event.ordering_key or "",
            **attrs,
        )
        futures.append((event.event_id, future))
    published = [
        {"event_id": event_id, "message_id": future.result()}
        for event_id, future in futures
    ]
    return {
        "provider": "google-cloud-pubsub",
        "topic": topic_path(),
        "published": published,
    }
