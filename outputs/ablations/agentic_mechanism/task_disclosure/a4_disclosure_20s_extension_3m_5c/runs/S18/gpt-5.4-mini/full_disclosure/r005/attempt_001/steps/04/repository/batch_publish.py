from __future__ import annotations

import json
import os
from typing import Any, Iterable, Mapping, Sequence

from google.cloud import pubsub_v1


def _publisher_client() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


def _build_message(data: Any, attributes: Mapping[str, str] | None = None) -> pubsub_v1.PubsubMessage:
    if isinstance(data, bytes):
        payload = data
    elif isinstance(data, str):
        payload = data.encode("utf-8")
    else:
        payload = json.dumps(data, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return pubsub_v1.PubsubMessage(data=payload, attributes=dict(attributes or {}))


def batch_publish(
    topic_path: str | None = None,
    messages: Sequence[Mapping[str, Any]] | None = None,
) -> list[str]:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GOOGLE_PROJECT_ID")
    if topic_path is None:
        topic_name = os.environ.get("PUBSUB_TOPIC")
        if not project_id or not topic_name:
            raise ValueError("Provide topic_path or set GOOGLE_CLOUD_PROJECT and PUBSUB_TOPIC")
        topic_path = f"projects/{project_id}/topics/{topic_name}"
    if not messages:
        return []

    publisher = _publisher_client()
    publish_futures = []
    for item in messages:
        data = item.get("data")
        attributes = item.get("attributes")
        message = _build_message(data, attributes)
        publish_futures.append(publisher.publish(topic_path, message.data, **message.attributes))

    return [future.result() for future in publish_futures]


def publish_batch_with_ids(topic_path: str, messages: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    message_ids = batch_publish(topic_path=topic_path, messages=messages)
    return {"provider": "google_cloud_pubsub", "topic_path": topic_path, "message_ids": message_ids}


__all__ = ["batch_publish", "publish_batch_with_ids"]
