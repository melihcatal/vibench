from google.cloud import pubsub_v1
import os
import json

def batch_publish(project_id: str, topic_id: str, messages: list[dict]) -> list[str]:
    """Publishes a batch of messages to a Google Cloud Pub/Sub topic."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    
    futures = []
    for message in messages:
        message_json = json.dumps(message["data"]).encode("utf-8")
        attributes = message.get("attributes", {})
        futures.append(publisher.publish(topic_path, message_json, **attributes))
    
    return [future.result() for future in futures]

if __name__ == "__main__":
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    TOPIC_ID = os.getenv("GOOGLE_CLOUD_PUBSUB_TOPIC_ID")

    if not PROJECT_ID or not TOPIC_ID:
        print("Please set GOOGLE_CLOUD_PROJECT_ID and GOOGLE_CLOUD_PUBSUB_TOPIC_ID environment variables.")
    else:
        test_messages = [
            {"data": {"event": "batch_event_1", "value": 1}, "attributes": {"source": "app1"}},
            {"data": {"event": "batch_event_2", "value": 2}, "attributes": {"source": "app2"}},
            {"data": {"event": "batch_event_3", "value": 3}, "attributes": {"source": "app1"}},
        ]
        message_ids = batch_publish(PROJECT_ID, TOPIC_ID, test_messages)
        print(f"Published batch messages with IDs: {message_ids}")
