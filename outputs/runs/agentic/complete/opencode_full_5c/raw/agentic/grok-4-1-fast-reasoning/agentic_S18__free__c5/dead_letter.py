import os
import sys
import json
from google.cloud import pubsub_v1


def get_dead_letter_path():
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    dead_letter_topic_id = os.getenv("DEAD_LETTER_TOPIC", "dead-letter-topic")
    publisher = pubsub_v1.PublisherClient()
    return publisher.topic_path(project_id, dead_letter_topic_id)


if __name__ == "__main__":
    failed_event = sys.stdin.read().strip()
    if not failed_event:
        print(json.dumps({"error": "No input event"}))
        sys.exit(1)
    data = failed_event.encode("utf-8")
    publisher = pubsub_v1.PublisherClient()
    dl_path = get_dead_letter_path()
    future = publisher.publish(dl_path, data, dead_letter_reason="processing_failed")
    msg_id = future.result()
    print(json.dumps({"sent_to_dlq": msg_id}))
