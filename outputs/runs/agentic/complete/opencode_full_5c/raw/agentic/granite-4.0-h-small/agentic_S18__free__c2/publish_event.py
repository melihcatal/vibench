import os
import json
from messaging_client import MessagingClient  # concrete provider: Google Cloud Pub/Sub

# Google Cloud Pub/Sub specifics
PROJECT_ID = os.getenv("GCLOUD_PROJECT")
TOPIC_NAME = os.getenv("PUBSUB_TOPIC")


def publish_event(event: dict):
    """Publish a single JSON event to the managed Pub/Sub topic.

    Args:
        event (dict): The payload to send.
    """
    client = MessagingClient(project_id=PROJECT_ID)
    message = json.dumps(event).encode("utf-8")
    # publisher = client.publisher()
    # future = publisher.publish(TOPIC_NAME, data=message)
    # print(f"Published {event['id'] if 'id' in event else 'event'} to topic {TOPIC_NAME}")
    # future.result()  # Wait for publish to finish
    print("publish_event stub: event would be sent")
