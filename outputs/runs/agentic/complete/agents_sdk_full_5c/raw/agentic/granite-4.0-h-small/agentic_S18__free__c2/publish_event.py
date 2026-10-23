import os
import json
from google.cloud import pubsub_v1

# Use Google Cloud Pub/Sub as the concrete provider
PROJECT_ID = os.getenv('GCP_PROJECT_ID')
TOPIC_ID = os.getenv('PUBSUB_TOPIC_ID')

# Helper function to publish a JSON event
def publish_event(event: dict) -> str:
    """Publish a JSON event to a Pub/Sub topic and return the message ID.

    Args:
        event (dict): The event payload to publish.
    """
    # Create a publisher client
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)
    # Serialize the event to JSON bytes
    data = json.dumps(event).encode('utf-8')
    # Publish the message
    future = publisher.publish(topic_path, data=data)
    msg_id = future.result()
    return msg_id

def main():
    sample_event = {
        "type": "order_created",
        "order_id": "12345",
        "customer": "alice@example.com"
    }
    msg_id = publish_event(sample_event)
    print(f"Published event with ID: {msg_id}")

if __name__ == "__main__":
    main()