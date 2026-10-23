import json
import os
import uuid
from datetime import datetime
from google.cloud import pubsub_v1


def publish_batch(messages, topic_id=None, batch_settings=None):
    """Publish a batch of messages to Google Cloud Pub/Sub with IDs and attributes."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-project-id")
    if topic_id is None:
        topic_id = os.environ.get("PUBSUB_TOPIC_ID", "event-topic")

    if batch_settings is None:
        batch_settings = {
            "max_messages": 100,
            "max_bytes": 1 * 1024 * 1024,
            "max_latency": 1,
        }

    publisher_options = pubsub_v1.types.PublisherOptions(enable_message_ordering=False)

    batch_settings_obj = pubsub_v1.types.BatchSettings(
        max_messages=batch_settings["max_messages"],
        max_bytes=batch_settings["max_bytes"],
        max_latency=batch_settings["max_latency"],
    )

    publisher = pubsub_v1.PublisherClient(
        publisher_options=publisher_options, batch_settings=batch_settings_obj
    )

    topic_path = publisher.topic_path(project_id, topic_id)

    futures = []
    results = []

    for i, message in enumerate(messages):
        if isinstance(message, dict):
            message["batch_id"] = str(uuid.uuid4())
            message["batch_index"] = i
            message["published_at"] = datetime.utcnow().isoformat()
            data = json.dumps(message).encode("utf-8")
            attributes = {"batch_index": str(i), "message_type": "batch"}
        else:
            data = message.encode("utf-8") if isinstance(message, str) else message
            attributes = {"batch_index": str(i), "message_type": "batch"}

        future = publisher.publish(topic_path, data, **attributes)
        futures.append(future)

    for i, future in enumerate(futures):
        try:
            message_id = future.result(timeout=30.0)
            results.append(
                {
                    "message_id": message_id,
                    "batch_index": i,
                    "status": "published",
                    "provider": "google-cloud-pubsub",
                }
            )
        except Exception as e:
            results.append(
                {
                    "message_id": None,
                    "batch_index": i,
                    "status": "failed",
                    "error": str(e),
                    "provider": "google-cloud-pubsub",
                }
            )

    return {
        "total_messages": len(messages),
        "published": len([r for r in results if r["status"] == "published"]),
        "failed": len([r for r in results if r["status"] == "failed"]),
        "results": results,
        "topic": topic_path,
        "provider": "google-cloud-pubsub",
    }


if __name__ == "__main__":
    batch_messages = [
        {"user_id": f"user_{i}", "action": "view", "page": f"page_{i}"}
        for i in range(5)
    ]
    result = publish_batch(batch_messages)
    print(f"Batch publish result: {result}")
