import json
import os
import sys

from google.cloud import pubsub_v1


def _parse_messages(raw: str):
    messages = json.loads(raw)
    if not isinstance(messages, list):
        raise ValueError("BATCH_MESSAGES must be a JSON list")
    return messages


def batch_publish(topic_path: str, messages):
    publisher = pubsub_v1.PublisherClient()
    futures = []
    for message in messages:
        if not isinstance(message, dict):
            raise ValueError("Each batch message must be an object")
        payload = message.get("data", message)
        data = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        attrs = {k: str(v) for k, v in message.get("attributes", {}).items()}
        futures.append(publisher.publish(topic_path, data=data, **attrs))
    return [future.result() for future in futures]


def main() -> int:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCLOUD_PROJECT")
    topic_id = os.environ.get("PUBSUB_TOPIC")
    if not project_id or not topic_id:
        raise SystemExit("GOOGLE_CLOUD_PROJECT and PUBSUB_TOPIC are required")

    raw_messages = os.environ.get("BATCH_MESSAGES")
    if raw_messages:
        messages = _parse_messages(raw_messages)
    else:
        messages = [
            {"id": "msg-1", "attributes": {"source": "batch_publish.py"}},
            {"id": "msg-2", "attributes": {"source": "batch_publish.py"}},
        ]

    topic_path = pubsub_v1.PublisherClient().topic_path(project_id, topic_id)
    message_ids = batch_publish(topic_path, messages)
    sys.stdout.write(json.dumps(message_ids))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
