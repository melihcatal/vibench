import json
import os
from google.cloud import pubsub_v1
from messaging_client import load_config, topic_path, normalize_attributes
from messaging_models import to_json_bytes, BatchPublishItem


def batch_publish(items: list[dict]):
    config = load_config()
    client = pubsub_v1.PublisherClient()
    path = topic_path(config.project_id, config.topic_id)
    results = []
    for item in items:
        payload = BatchPublishItem(
            message_id=item["message_id"],
            payload=item["payload"],
            attributes=item.get("attributes", {}),
        )
        future = client.publish(
            path,
            to_json_bytes(payload.payload),
            **normalize_attributes(payload.attributes),
        )
        results.append({"message_id": payload.message_id, "pubsub_id": future.result()})
    return results


if __name__ == "__main__":
    print(
        json.dumps(
            batch_publish(json.loads(os.getenv("BATCH_JSON", "[]"))), sort_keys=True
        )
    )
