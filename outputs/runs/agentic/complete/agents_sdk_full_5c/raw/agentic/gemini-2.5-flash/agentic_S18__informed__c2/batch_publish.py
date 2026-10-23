from google.cloud import pubsub_v1
import json
import os

def publish_batch_events(project_id: str, topic_id: str, messages: list[dict]):
    """Publishes a batch of JSON events to a Pub/Sub topic."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    futures = []
    for i, data in enumerate(messages):
        json_data = json.dumps(data).encode("utf-8")
        # You can add custom attributes here if needed
        future = publisher.publish(topic_path, json_data, message_id=str(i))
        futures.append(future)

    print(f"Published {len(messages)} messages. Waiting for results...")
    results = []
    for i, future in enumerate(futures):
        try:
            message_id = future.result()
            results.append(f"Message {i} published with ID: {message_id}")
        except Exception as e:
            results.append(f"Error publishing message {i}: {e}")
            print(f"Error publishing message {i}: {e}")

    for result in results:
        print(result)

    return results

if __name__ == "__main__":
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    topic_id = os.getenv("GOOGLE_CLOUD_PUBSUB_TOPIC_ID_BATCH_PUBLISH")
    
    batch_data = [
        {"order_id": "1001", "status": "new", "product": "A"},
        {"order_id": "1002", "status": "new", "product": "B"},
        {"order_id": "1003", "status": "new", "product": "C"},
    ]

    if not all([project_id, topic_id]):
        print("Please set GOOGLE_CLOUD_PROJECT_ID and GOOGLE_CLOUD_PUBSUB_TOPIC_ID_BATCH_PUBLISH environment variables.")
    else:
        publish_batch_events(project_id, topic_id, batch_data)
