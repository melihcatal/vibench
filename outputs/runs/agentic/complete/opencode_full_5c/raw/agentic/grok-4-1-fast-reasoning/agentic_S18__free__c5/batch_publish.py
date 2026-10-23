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
    batch_json = sys.stdin.read().strip()
    if not batch_json:
        print(json.dumps({"error": "No input batch"}))
        sys.exit(1)
    batch_data = json.loads(batch_json)
    events = batch_data.get("events", [])
    publisher = pubsub_v1.PublisherClient()
    topic_path = get_topic_path()
    published_ids = []
    for i, event in enumerate(events):
        data = json.dumps(event).encode("utf-8")
        future = publisher.publish(topic_path, data, batch_index=str(i))
        published_ids.append(future.result())
    print(json.dumps({"published_message_ids": published_ids}))
