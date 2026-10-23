import json
import os
import sys

from google.cloud import pubsub_v1


def main() -> None:
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    topic_id = os.environ["PUBSUB_TOPIC_ID"]
    event = json.loads(sys.stdin.read() or "{}")

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    data = json.dumps(event).encode("utf-8")
    future = publisher.publish(topic_path, data=data, content_type="application/json")
    message_id = future.result()
    sys.stdout.write(message_id)


if __name__ == "__main__":
    main()
