from __future__ import annotations

from typing import Iterable, Mapping, Sequence

from google.cloud import pubsub_v1

from messaging_client import load_config, publisher_client, topic_path
from messaging_models import BatchPublishResult, build_envelope


def batch_publish(messages: Sequence[Mapping[str, object]]) -> BatchPublishResult:
    topic = topic_path()
    futures = []
    for item in messages:
        envelope = build_envelope(
            message_id=str(item.get("id", "")),
            payload=item.get("payload", {}),
            attributes=item.get("attributes", {}),
        )
        futures.append(publisher_client().publish(topic, envelope.to_json_bytes(), **envelope.attributes))
    message_ids = [future.result() for future in futures]
    return BatchPublishResult(message_ids=message_ids, topic=topic)


if __name__ == "__main__":
    batch_publish(
        [
            {"id": "msg-1", "payload": {"kind": "create"}, "attributes": {"source": "batch"}},
            {"id": "msg-2", "payload": {"kind": "update"}, "attributes": {"source": "batch"}},
        ]
    )
