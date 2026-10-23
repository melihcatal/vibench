from google.cloud import pubsub_v1
import os
import json

def batch_publish(project_id: str, topic_id: str, messages: list):
    """Publishes a batch of messages to a Pub/Sub topic."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    
    publish_futures = []
    for message_data in messages:
        message_json = json.dumps(message_data["data"]).encode("utf-8")
        attributes = message_data.get("attributes", {})
        
        future = publisher.publish(topic_path, message_json, **attributes)
        publish_futures.append(future)

    # Wait for all messages in the batch to be published
    for future in publish_futures:
        print(f"Published message ID: {future.result()}")

if __name__ == '__main__':
    # Example usage
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    TOPIC_ID = os.getenv("PUBSUB_TOPIC_ID", "my-test-topic")
    
    if not PROJECT_ID:
        print("Please set the GOOGLE_CLOUD_PROJECT_ID environment variable.")
    else:
        sample_messages = [
            {"data": {"order_id": "1001", "status": "new"}, "attributes": {"type": "order"}},
            {"data": {"order_id": "1002", "status": "processing"}, "attributes": {"type": "order"}},
            {"data": {"user_id": "500", "action": "login"}, "attributes": {"type": "user_event"}},
        ]
        batch_publish(PROJECT_ID, TOPIC_ID, sample_messages)
