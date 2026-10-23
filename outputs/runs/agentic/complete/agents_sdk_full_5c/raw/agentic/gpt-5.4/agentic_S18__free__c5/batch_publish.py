from __future__ import annotations

from typing import Any, Dict, Iterable, List

from messaging_client import publisher_client, topic_path
from messaging_models import MessagePayload


def batch_publish(messages: Iterable[Dict[str, Any]]) -> List[Dict[str, str]]:
    client = publisher_client()
    futures = []
    tracked: List[MessagePayload] = []
    for item in messages:
        payload = MessagePayload(
            body=item.get("body", {}),
            attributes=item.get("attributes", {}),
            ordering_key=item.get("ordering_key"),
            message_id=item.get("message_id"),
        )
        payload.ensure_id()
        tracked.append(payload)
        future = client.publish(
            topic_path(),
            payload.to_json_bytes(),
            message_id=payload.message_id,
            **payload.attributes,
            **({"ordering_key": payload.ordering_key} if payload.ordering_key else {}),
        )
        futures.append(future)
    results = []
    for payload, future in zip(tracked, futures):
        results.append(
            {
                "provider": "google-cloud-pubsub",
                "topic": topic_path(),
                "client_message_id": payload.message_id or "",
                "published_message_id": future.result(timeout=30),
            }
        )
    return results
