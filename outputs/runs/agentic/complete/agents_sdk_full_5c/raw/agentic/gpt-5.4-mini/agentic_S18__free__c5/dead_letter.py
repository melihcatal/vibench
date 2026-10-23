import json
import sys
from typing import Any, Dict

from google.cloud import pubsub_v1

from messaging_client import get_project_id, get_publisher_client, resolve_dlq_topic_id, topic_path
from messaging_models import MessagePayload, PublishOutcome


def dead_letter(message: Dict[str, Any], project_id: str | None = None, dlq_topic_id: str | None = None) -> PublishOutcome:
    project = get_project_id(project_id)
    dlq_topic = resolve_dlq_topic_id(dlq_topic_id)
    client: pubsub_v1.PublisherClient = get_publisher_client()
    path = topic_path(project, dlq_topic)
    attributes = {"dead_letter": "true"}
    if isinstance(message.get("attributes"), dict):
        attributes.update({str(k): str(v) for k, v in message["attributes"].items()})
    payload = MessagePayload(message_id=str(message.get("message_id") or message.get("id") or "dead-letter"), payload=message, attributes=attributes)
    future = client.publish(path, payload.to_json_bytes(), **payload.attributes)
    return PublishOutcome(message_ids=[future.result()], topic=path)


if __name__ == "__main__":
    raw = sys.stdin.read().strip() or "{}"
    message = json.loads(raw)
    outcome = dead_letter(message)
    print(json.dumps({"topic": outcome.topic, "message_ids": outcome.message_ids}, ensure_ascii=False))
