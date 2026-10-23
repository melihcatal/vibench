import os
import json
import uuid
from google.cloud import pubsub_v1
from messaging_client import get_publisher_client, get_topic_path

def publish_message_batch(messages: list[dict]):
    """
    Publishes a batch of messages to a Pub/Sub topic.
    Each message can have its own attributes.
    """
    publisher, topic_path = get_publisher_client()
    publish_futures = []

    for msg_data in messages:
        payload = json.dumps(msg_data["payload"]).encode("utf-8")
        attributes = msg_data.get("attributes", {})
        
        # The Pub/Sub client library automatically batches messages.
        # We just call publish repeatedly.
        future = publisher.publish(topic_path, payload, **attributes)
        publish_futures.append(future)

    # Wait for all the publish futures to resolve.
    results = [future.result() for future in publish_futures]
    print(f"Published {len(results)} messages in a batch.")
    return results

if __name__ == '__main__':
    if os.getenv("GCP_PROJECT_ID"):
        # Example batch
        message_batch = [
            {
                "payload": {"item_id": "SKU-001", "quantity": 10},
                "attributes": {"event_type": "inventory_update", "source": "pos-terminal-1"}
            },
            {
                "payload": {"item_id": "SKU-002", "quantity": 5},
                "attributes": {"event_type": "inventory_update", "source": "pos-terminal-2"}
            },
            {
                "payload": {"customer_id": "C-567", "status": "shipped"},
                "attributes": {"event_type": "order_status", "correlation_id": str(uuid.uuid4())}
            }
        ]
        publish_message_batch(message_batch)
    else:
        print("Set GCP_PROJECT_ID and other env vars to run.")
