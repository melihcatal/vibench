import json
from google.cloud import pubsub_v1
from messaging_client import get_publisher_client
from messaging_models import MessagePayload

# Google Cloud Pub/Sub project and topic ID
PROJECT_ID = 'your-gcp-project-id'
TOPIC_ID = 'your-topic-id'

def publish_event(event: dict, message_id: str = None):
    """Publish a single JSON event to a Pub/Sub topic.

    Args:
        event (dict): The JSON payload to publish.
        message_id (str, optional): Optional custom message ID.
    """
    # Ensure payload conforms to our normalized model
    payload = MessagePayload(**event)
    publisher = get_publisher_client()
    data = json.dumps(payload.dict()).encode('utf-8')
    future = publisher.publish(TOPIC_ID, data=data, msg_id=message_id)
    print(f"Published event {payload.event_id} with future: {future}")

if __name__ == '__main__':
    sample_event = {
        "event_id": "test-001",
        "timestamp": "2025-08-14T12:00:00Z",
        "data": {"key": "value"}
    }
    publish_event(sample_event)
