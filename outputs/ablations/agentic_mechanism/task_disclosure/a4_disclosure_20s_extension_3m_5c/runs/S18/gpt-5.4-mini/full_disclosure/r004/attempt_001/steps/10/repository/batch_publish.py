import json
import os
from typing import Any, Dict, Iterable, List, Optional

from google.cloud import pubsub_v1


def _publisher_client() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


def _topic_path(topic_id: str) -> str:
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    return _publisher_client().topic_path(project_id, topic_id)


def _encode_message(message: Dict[str, Any]) -> bytes:
    payload = message.get("data", message)
    if isinstance(payload, (dict, list)):
        return json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    if isinstance(payload, str):
        return payload.encode("utf-8")
    return json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _message_attributes(message: Dict[str, Any]) -> Dict[str, str]:
    attributes = dict(message.get("attributes") or {})
    message_id = message.get("id")
    if message_id is not None:
        attributes.setdefault("message_id", str(message_id))
    for key in ("event_id", "correlation_id", "source"):
        value = message.get(key)
        if value is not None:
            attributes.setdefault(key, str(value))
    return attributes


def publish_batch(topic_path: str, messages: Iterable[Dict[str, Any]]) -> List[str]:
    client = _publisher_client()
    futures = []
    for message in messages:
        futures.append(client.publish(topic_path, _encode_message(message), **_message_attributes(message)))
    return [future.result() for future in futures]


def main() -> None:
    topic_id = os.environ["PUBSUB_TOPIC"]
    topic_path = _topic_path(topic_id)
    messages = json.loads(os.environ.get("BATCH_MESSAGES_JSON", "[]"))
    message_ids = publish_batch(topic_path, messages)
    print(json.dumps({"message_ids": message_ids}))


if __name__ == "__main__":
    main()
