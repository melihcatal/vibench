import json
from messaging_client import get_publisher_client, get_topic_path
from messaging_models import Message


def publish_event(topic_id: str, event_data: dict, attributes: dict = None):
    publisher = get_publisher_client()
    topic_path = get_topic_path(topic_id)

    data = json.dumps(event_data).encode("utf-8")
    future = publisher.publish(topic_path, data, **(attributes or {}))
    print(f"Published message ID: {future.result()}")
    return future.result()


if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_CLOUD_PROJECT environment variable
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable to your service account key file path
    # Make sure to create a topic named 'my-test-topic' in your Google Cloud Project
    # from your terminal: export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    # from your terminal: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    # Example event data
    example_event = {
        "type": "user_registered",
        "user_id": "123",
        "email": "test@example.com",
    }
    example_attributes = {"origin": "website", "source_ip": "192.168.1.1"}

    # Replace 'my-test-topic' with your actual Pub/Sub topic ID
    publish_event("my-test-topic", example_event, example_attributes)
