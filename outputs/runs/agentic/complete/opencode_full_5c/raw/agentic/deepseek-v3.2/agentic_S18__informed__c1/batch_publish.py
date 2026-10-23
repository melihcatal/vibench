import os
import json
import uuid
from google.cloud import pubsub_v1


def batch_publish(messages, topic_id=None):
    """Publish a batch of messages with IDs to Google Cloud Pub/Sub."""
    if topic_id is None:
        topic_id = os.getenv("PUBSUB_TOPIC_ID", "event-topic")

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set")

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    futures = []
    results = []

    for i, message in enumerate(messages):
        if isinstance(message, dict):
            if "id" not in message:
                message["batch_id"] = str(uuid.uuid4())
            data = json.dumps(message).encode("utf-8")
        else:
            message_dict = {"data": str(message), "batch_id": str(uuid.uuid4())}
            data = json.dumps(message_dict).encode("utf-8")

        attributes = {"batch_index": str(i), "total_messages": str(len(messages))}

        future = publisher.publish(topic_path, data, **attributes)
        futures.append(future)

    for future in futures:
        try:
            message_id = future.result()
            results.append({"message_id": message_id, "status": "published"})
        except Exception as e:
            results.append({"message_id": None, "status": "failed", "error": str(e)})

    return {
        "total_messages": len(messages),
        "published": len([r for r in results if r["status"] == "published"]),
        "failed": len([r for r in results if r["status"] == "failed"]),
        "results": results,
    }
