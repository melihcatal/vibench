
from google.cloud import pubsub_v1
import os

# Set your Google Cloud Project ID and Pub/Sub Topic ID
project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
topic_id = "your-topic-id"  # Replace with your Pub/Sub topic ID

if not project_id:
    raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

messages = [
    {"data": "Hello World 1", "message_id": "msg-001"},
    {"data": "Hello World 2", "attributes": {"origin": "python-script"}},
    {"data": "Hello World 3"},
]

def publish_batch_messages(messages):
    futures = []
    for msg in messages:
        data = msg["data"].encode("utf-8")
        if "message_id" in msg:
            # Note: message_id is usually assigned by the server.
            # You can set ordering_key for ordered messages.
            # For this example, we'll just publish data and attributes.
            print(f"Publishing message with data: {msg['data']}")
            future = publisher.publish(topic_path, data)
        elif "attributes" in msg:
            print(f"Publishing message with data: {msg['data']} and attributes: {msg['attributes']}")
            future = publisher.publish(topic_path, data, **msg["attributes"])
        else:
            print(f"Publishing message with data: {msg['data']}")
            future = publisher.publish(topic_path, data)
        futures.append(future)

    for future in futures:
        try:
            message_id = future.result()
            print(f"Published message with ID: {message_id}")
        except Exception as e:
            print(f"Error publishing message: {e}")

if __name__ == "__main__":
    print(f"Using Google Cloud Project: {project_id}")
    print(f"Publishing to Pub/Sub Topic: {topic_path}")
    publish_batch_messages(messages)
