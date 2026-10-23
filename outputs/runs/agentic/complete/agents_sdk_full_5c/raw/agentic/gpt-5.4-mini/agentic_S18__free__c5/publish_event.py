import json
import sys
from typing import Any, Dict

from google.cloud import pubsub_v1

from messaging_client import get_project_id, get_publisher_client, resolve_topic_id, topic_path
from messaging_models import MessagePayload, PublishOutcome


def publish_event(event: Dict[str, Any], project_id: str | None = None, topic_id: str | None = None) -> PublishOutcome:
    project = get_project_id(project_id)
    topic = resolve_topic_id(topic_id)
    client: pubsub_v1.PublisherClient = get_publisher_client()
    path = topic_path(project, topic)
    payload = MessagePayload(
        message_id=str(event.get("message_id") or event.get("id") or "unknown"),
        payload=event,
        attributes={k: str(v) for k, v in event.get("attributes", {}).items()} if isinstance(event.get("attributes"), dict) else {},
    )
    future = client.publish(path, payload.to_json_bytes(), **payload.attributes)
    message_id = future.result()
    return PublishOutcome(message_ids=[message_id], topic=path)


if __name__ == "__main__":
    raw = sys.stdin.read().strip() or "{}"
    event = json.loads(raw)
    outcome = publish_event(event)
    print(json.dumps({"topic": outcome.topic, "message_ids": outcome.message_ids}, ensure_ascii=False))
