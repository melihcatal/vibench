import json
import sys
from typing import Any, Dict, Iterable, List

from google.cloud import pubsub_v1

from messaging_client import get_project_id, get_publisher_client, resolve_topic_id, topic_path
from messaging_models import MessagePayload, PublishOutcome


def batch_publish(messages: Iterable[Dict[str, Any]], project_id: str | None = None, topic_id: str | None = None) -> PublishOutcome:
    project = get_project_id(project_id)
    topic = resolve_topic_id(topic_id)
    client: pubsub_v1.PublisherClient = get_publisher_client()
    path = topic_path(project, topic)
    ids: List[str] = []
    for index, message in enumerate(messages):
        attributes = {str(k): str(v) for k, v in message.get("attributes", {}).items()} if isinstance(message.get("attributes"), dict) else {}
        attributes.setdefault("batch_index", str(index))
        payload = MessagePayload(message_id=str(message.get("message_id") or message.get("id") or f"msg-{index}"), payload=message, attributes=attributes)
        ids.append(client.publish(path, payload.to_json_bytes(), **payload.attributes).result())
    return PublishOutcome(message_ids=ids, topic=path)


if __name__ == "__main__":
    raw = sys.stdin.read().strip() or "[]"
    messages = json.loads(raw)
    outcome = batch_publish(messages)
    print(json.dumps({"topic": outcome.topic, "message_ids": outcome.message_ids}, ensure_ascii=False))
