import json
import os
import sys

from google.cloud import pubsub_v1


def publish_event(topic_path: str, event: dict) -> str:
    publisher = pubsub_v1.PublisherClient()
    data = json.dumps(event, separators=(",", ":")).encode("utf-8")
    future = publisher.publish(topic_path, data=data, content_type="application/json")
    return future.result()


def main() -> int:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCLOUD_PROJECT")
    topic_id = os.environ.get("PUBSUB_TOPIC")
    if not project_id or not topic_id:
        raise SystemExit("GOOGLE_CLOUD_PROJECT and PUBSUB_TOPIC are required")

    event_json = os.environ.get("EVENT_JSON")
    if event_json:
        event = json.loads(event_json)
    else:
        event = {
            "type": "example.event",
            "source": "publish_event.py",
            "payload": {"message": "hello"},
        }

    topic_path = pubsub_v1.PublisherClient().topic_path(project_id, topic_id)
    message_id = publish_event(topic_path, event)
    sys.stdout.write(message_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
