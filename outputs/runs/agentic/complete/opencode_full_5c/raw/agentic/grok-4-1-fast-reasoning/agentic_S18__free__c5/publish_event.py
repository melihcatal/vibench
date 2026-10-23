import os
import sys
import json
from google.cloud import pubsub_v1


def get_topic_path():
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    topic_id = os.getenv("PUBSUB_TOPIC", "events-topic")
    publisher = pubsub_v1.PublisherClient()
    return publisher.topic_path(project_id, topic_id)


if __name__ == "__main__":
    event_json = sys.stdin.read().strip()
    if not event_json:
        print(json.dumps({"error": "No input event"}))
        sys.exit(1)
    data = event_json.encode("utf-8")
    publisher = pubsub_v1.PublisherClient()
    topic_path = get_topic_path()
    future = publisher.publish(topic_path, data)
    msg_id = future.result()
    print(json.dumps({"published_message_id": msg_id}))
