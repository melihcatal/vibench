import json
import os
from google.cloud import pubsub_v1

def publish_batch_events(project_id: str, topic_id: str, events: list):
    """
    Publishes a batch of JSON events to a Google Cloud Pub/Sub topic.
    Each event in the list should be a dictionary.
    """
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    futures = []
    for event_data in events:
        data = json.dumps(event_data).encode("utf-8")
        # You can add attributes here if needed, e.g., for routing or filtering
        future = publisher.publish(topic_path, data, event_type="batch_event")
        futures.append(future)

    print(f"Published {len(futures)} messages in a batch.")
    # Wait for all published messages to be acknowledged by the Pub/Sub service
    results = [future.result() for future in futures]
    print(f"Batch publish results: {results}")
    return results

if __name__ == "__main__":
    # For demonstration purposes
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
    TOPIC_ID = "my-batch-topic" # Ensure this topic exists

    sample_events = [
        {"id": "batch-1", "action": "create", "payload": {"item": "apple"}},
        {"id": "batch-2", "action": "update", "payload": {"item": "banana", "quantity": 10}},
        {"id": "batch-3", "action": "delete", "payload": {"item": "orange"}}
    ]

    if PROJECT_ID:
        publish_batch_events(PROJECT_ID, TOPIC_ID, sample_events)
    else:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
