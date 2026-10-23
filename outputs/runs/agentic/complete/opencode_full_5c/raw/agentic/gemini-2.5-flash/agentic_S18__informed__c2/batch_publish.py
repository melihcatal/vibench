import json
from messaging_client import get_publisher_client, get_topic_path
from messaging_models import Message


def batch_publish_events(topic_id: str, event_list: list[dict]):
    publisher = get_publisher_client()
    topic_path = get_topic_path(topic_id)

    futures = []
    for event_data in event_list:
        data = json.dumps(event_data["data"]).encode("utf-8")
        attributes = event_data.get("attributes", {})
        future = publisher.publish(topic_path, data, **attributes)
        futures.append(future)

    for future in futures:
        print(f"Published message ID: {future.result()}")

    return [f.result() for f in futures]


if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_CLOUD_PROJECT environment variable
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable to your service account key file path
    # Make sure to create a topic named 'my-test-topic' in your Google Cloud Project
    # from your terminal: export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    # from your terminal: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    # Example list of events
    events_to_publish = [
        {
            "data": {"type": "product_viewed", "product_id": "A1", "user_id": "user_1"},
            "attributes": {"session_id": "sess_001"},
        },
        {
            "data": {"type": "product_added", "product_id": "B2", "user_id": "user_1"},
            "attributes": {"session_id": "sess_001"},
        },
        {
            "data": {"type": "checkout_started", "user_id": "user_2"},
            "attributes": {"session_id": "sess_002"},
        },
    ]

    # Replace 'my-test-topic' with your actual Pub/Sub topic ID
    batch_publish_events("my-test-topic", events_to_publish)
