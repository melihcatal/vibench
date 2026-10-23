
import os
import json
from google.cloud import pubsub_v1
from messaging_client import get_publisher_client, project_id, topic_id
from messaging_models import EventPayload

def publish_event(payload: EventPayload):
    """Publishes a single event to a Google Cloud Pub/Sub topic."""
    publisher = get_publisher_client()
    topic_path = publisher.topic_path(project_id, topic_id)

    data = payload.model_dump_json().encode("utf-8")

    future = publisher.publish(topic_path, data)
    print(f"Published message {future.result()} to {topic_path}")
    return future.result()

if __name__ == "__main__":
    # This is an example, not part of the required functionality.
    # To run, ensure you have set up Google Cloud authentication
    # and the required environment variables in messaging_client.py
    if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        sample_payload = EventPayload(
            request_id="req-123",
            user_id="user-456",
            data={"message": "Hello, Pub/Sub!"}
        )
        publish_event(sample_payload)
