import os
import json
import uuid
from typing import List, Dict, Any
from google.cloud import pubsub_v1


def batch_publish(topic_name, messages: List[Dict[str, Any]]):
    """Publish a batch of messages with IDs or attributes to Google Cloud Pub/Sub."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set")

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)

    batch_settings = pubsub_v1.types.BatchSettings(
        max_messages=100, max_bytes=1 * 1024 * 1024, max_latency=1
    )

    results = []

    for message in messages:
        message_id = message.get("id", str(uuid.uuid4()))
        data = message.get("data", {})
        attributes = message.get("attributes", {})

        if isinstance(data, dict):
            data_bytes = json.dumps(data).encode("utf-8")
        else:
            data_bytes = str(data).encode("utf-8")

        attributes["batch_message_id"] = message_id

        future = publisher.publish(topic_path, data_bytes, **attributes)
        message_id_result = future.result()

        results.append(
            {
                "batch_id": message_id,
                "pubsub_message_id": message_id_result,
                "attributes": attributes,
            }
        )

    return {"topic": topic_path, "batch_size": len(results), "results": results}
