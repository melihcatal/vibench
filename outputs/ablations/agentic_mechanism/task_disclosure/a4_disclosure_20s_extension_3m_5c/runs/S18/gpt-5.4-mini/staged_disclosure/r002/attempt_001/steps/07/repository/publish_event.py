import json
import os
import sys

from google.cloud import pubsub_v1


def publish_event(event: dict) -> str:
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    topic_id = os.environ["PUBSUB_TOPIC"]
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    data = json.dumps(event, separators=(",", ":")).encode("utf-8")
    future = publisher.publish(topic_path, data=data, content_type="application/json")
    return future.result()


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: publish_event.py '<json>'")
    event = json.loads(sys.argv[1])
    message_id = publish_event(event)
    sys.stdout.write(message_id)


if __name__ == "__main__":
    main()
