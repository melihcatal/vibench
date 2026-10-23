from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping, Sequence

from google.cloud import pubsub_v1


@dataclass
class BatchMessage:
    data: bytes | str
    message_id: str | None = None
    attributes: dict[str, str] = field(default_factory=dict)

    def normalized_data(self) -> bytes:
        return self.data if isinstance(self.data, bytes) else self.data.encode("utf-8")


@dataclass
class BatchPublishResult:
    topic_path: str
    message_ids: list[str]


def _normalize_message(item: Any) -> BatchMessage:
    if isinstance(item, BatchMessage):
        return item
    if isinstance(item, (bytes, str)):
        return BatchMessage(data=item)
    if isinstance(item, Mapping):
        data = item.get("data", "")
        message_id = item.get("message_id") or item.get("id")
        attributes = item.get("attributes") or {}
        if not isinstance(attributes, Mapping):
            raise TypeError("attributes must be a mapping")
        return BatchMessage(data=data, message_id=message_id, attributes=dict(attributes))
    raise TypeError("Unsupported message type")


def _build_topic_path(project_id: str, topic_id: str) -> str:
    return pubsub_v1.PublisherClient().topic_path(project_id, topic_id)


def publish_batch(
    messages: Sequence[Any],
    project_id: str | None = None,
    topic_id: str | None = None,
    topic_path: str | None = None,
) -> BatchPublishResult:
    if topic_path is None:
        project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
        topic_id = topic_id or os.environ.get("PUBSUB_TOPIC_ID")
        if not project_id or not topic_id:
            raise ValueError("project_id and topic_id are required when topic_path is not provided")
        topic_path = _build_topic_path(project_id, topic_id)

    publisher = pubsub_v1.PublisherClient()
    futures = []
    for item in messages:
        message = _normalize_message(item)
        future = publisher.publish(topic_path, message.normalized_data(), message_id=message.message_id or "", **message.attributes)
        futures.append(future)

    message_ids = [future.result() for future in futures]
    return BatchPublishResult(topic_path=topic_path, message_ids=message_ids)


def publish_batch_from_json(payload: str, project_id: str | None = None, topic_id: str | None = None, topic_path: str | None = None) -> BatchPublishResult:
    raw = json.loads(payload)
    if not isinstance(raw, list):
        raise ValueError("payload must be a JSON list of messages")
    return publish_batch(raw, project_id=project_id, topic_id=topic_id, topic_path=topic_path)
