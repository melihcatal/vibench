from google.cloud import pubsub_v1
import os
import json

def publish_batch_events(project_id: str, topic_id: str, events: list[dict]) -> list[str]:
    """Publishes a batch of JSON events to a Google Cloud Pub/Sub topic.
    Returns a list of message IDs for the published messages.
    """
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    futures = []
    for event_data in events:
        data_str = json.dumps(event_data)
        data = data_str.encode("utf-8")
        future = publisher.publish(topic_path, data)
        futures.append(future)

    # Wait for all the publish futures to resolve
    message_ids = [future.result() for future in futures]
    return message_ids

if __name__ == '__main__':
    # Example usage:
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
    TOPIC_ID = os.getenv("PUBSUB_TOPIC_ID", "my-event-topic")
    batch_of_events = [
        {"message": "Batch message 1", "seq": 1},
        {"message": "Batch message 2", "seq": 2},
        {"message": "Batch message 3", "seq": 3}
    ]
    
    # print(f"Publishing batch of events to {TOPIC_ID}...")
    # ids = publish_batch_events(PROJECT_ID, TOPIC_ID, batch_of_events)
    # print(f"Published messages with IDs: {ids}")
