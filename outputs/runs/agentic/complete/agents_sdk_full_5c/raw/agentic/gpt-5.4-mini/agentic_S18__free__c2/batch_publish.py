from __future__ import annotations

import json
from typing import Any, Iterable, Sequence

from google.cloud import pubsub_v1

from messaging_client import load_config, publisher_client, topic_path
from messaging_models import PublishRequest, build_envelope


def batch_publish(events: Sequence[dict[str, Any]], project_id: str | None = None) -> list[str]:
    config = load_config(project_id)
    client = publisher_client()
    topic = topic_path(config)
    futures: list[Any] = []
    for index, event in enumerate(events):
        request = PublishRequest(
            payload=event,
            attributes={"batch_index": str(index), "source": "batch_publish.py"},
            ordering_key=str(event.get("ordering_key", "")),
            message_id=str(event.get("message_id", "")),
        )
        envelope = build_envelope(request)
        futures.append(client.publish(topic, envelope.to_json_bytes(), **envelope.attributes))
    return [future.result() for future in futures]
