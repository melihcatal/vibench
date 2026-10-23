import json
import os
import uuid
from google.cloud import pubsub_v1


def batch_publish(messages, topic_id=None):
    """Publish a batch of messages with IDs to Google Cloud Pub/Sub."""
    if topic_id is None:
        topic_id = os.environ.get(
            "PUBSUB_TOPIC_ID", "projects/my-project/topics/my-topic"
        )

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path("my-project", topic_id.split("/")[-1])

    futures = []
    message_ids = []

    for i, message in enumerate(messages):
        message_id = str(uuid.uuid4())
        attributes = {
            "message_id": message_id,
            "batch_index": str(i),
            "total_messages": str(len(messages)),
        }

        if isinstance(message, dict):
            data = json.dumps(message).encode("utf-8")
        else:
            data = str(message).encode("utf-8")

        future = publisher.publish(topic_path, data, **attributes)
        futures.append(future)
        message_ids.append(message_id)

    results = [future.result() for future in futures]

    return {
        "published_count": len(results),
        "message_ids": message_ids,
        "results": results,
    }
