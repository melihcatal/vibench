import os
from google.cloud import pubsub_v1

# Use Google Cloud Pub/Sub as the managed messaging service
# Environment variable points to the credentials
PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')
TOPIC_NAME = os.getenv('PUBSUB_TOPIC', 'my-topic')

# Helper utilities from local helpers
from messaging_client import get_publisher_client
from messaging_models import build_event_message

def publish_event(payload: dict, event_id: str = None):
    """Publish a JSON event to the Pub/Sub topic.

    Args:
        payload (dict): The event data to publish.
        event_id (str, optional): Custom message ID.
    """
    publisher = get_publisher_client()
    message = build_event_message(payload, event_id)
    future = publisher.publish(TOPIC_NAME, message)
    # Optional: block until acked
    try:
        response = future.result()
        print(f"Published message {response}.")
    except Exception as e:
        print(f"Error publishing message: {e}")

def main():
    sample_event = {
        'user_id': '12345',
        'action': 'login',
        'timestamp': '2025-08-27T12:00:00Z'
    }
    publish_event(sample_event)

if __name__ == '__main__':
    main()
