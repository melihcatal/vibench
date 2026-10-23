
import os
import json
from google.cloud import pubsub_v1
from messaging_client import get_publisher_client
from messaging_models import EventPayload

def publish_event_to_topic(event_payload: EventPayload):
    """
    Publishes a single JSON event to a Google Cloud Pub/Sub topic.

    Args:
        event_payload: An EventPayload object containing the event data.
    """
    publisher = get_publisher_client()
    topic_path = publisher.topic_path(os.environ["GCP_PROJECT_ID"], os.environ["GCP_TOPIC_ID"])

    # Prepare the message data
    data_str = json.dumps(event_payload.to_dict())
    data = data_str.encode("utf-8")

    # Publish the message
    future = publisher.publish(topic_path, data, correlation_id=event_payload.event_id)
    print(f"Published message {event_payload.event_id} with ID: {future.result()}")
    return future.result()

if __name__ == '__main__':
    # Example Usage:
    # Set the following environment variables before running:
    # export GCP_PROJECT_ID="your-gcp-project-id"
    # export GCP_TOPIC_ID="your-topic-id"
    
    # from uuid import uuid4
    # example_payload = EventPayload(
    #     event_id=str(uuid4()),
    #     user_id="user_123",
    #     data={"message": "Hello, Pub/Sub!"}
    # )
    # publish_event_to_topic(example_payload)
    pass
