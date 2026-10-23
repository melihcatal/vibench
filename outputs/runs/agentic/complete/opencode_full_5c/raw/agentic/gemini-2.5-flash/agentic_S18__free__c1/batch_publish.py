from messaging_client import get_publisher_client, get_topic_path, get_project_id
from messaging_models import EventMessage
import os
import time


def publish_batch_events(topic_id: str, events: list[dict]):
    """Publishes a batch of JSON events to a Google Cloud Pub/Sub topic.

    The Pub/Sub client library automatically handles batching.

    Args:
        topic_id: The ID of the Pub/Sub topic.
        events: A list of dictionaries, where each dictionary represents an event
                with 'data', 'type', and 'source' keys.
    """
    project_id = get_project_id()
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    publisher = get_publisher_client()
    topic_path = get_topic_path(project_id, topic_id)

    futures = []
    for event_data in events:
        event_type = event_data.get("type", "unknown")
        event_source = event_data.get("source", "batch_publisher")

        event_message = EventMessage(
            id=os.urandom(8).hex(),
            type=event_type,
            source=event_source,
            data=event_data["data"],
            attributes={"type": event_type, "source": event_source},
        )
        future = publisher.publish(
            topic_path, event_message.to_json(), **event_message.attributes
        )
        futures.append(future)

    for future in futures:
        # .result() blocks until the message is published
        print(f"Published message ID: {future.result()}")


if __name__ == "__main__":
    # Example Usage (replace with your actual topic_id and data)
    # Set GOOGLE_CLOUD_PROJECT environment variable before running
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    example_topic_id = "my-test-topic"
    example_events = [
        {
            "data": {"order_id": "1001", "item": "Laptop", "quantity": 1},
            "type": "order.created",
            "source": "order-service",
        },
        {
            "data": {"user_id": "456", "email": "new@example.com"},
            "type": "user.registered",
            "source": "auth-service",
        },
    ]

    # publish_batch_events(example_topic_id, example_events)
