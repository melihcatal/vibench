import os
from google.cloud import pubsub_v1

# Use Google Cloud Pub/Sub as the managed messaging service
# Environment variable points to the credentials
PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')
DLQ_TOPIC = os.getenv('PUBSUB_DEAD_LETTER_TOPIC', 'dead-letter')

# Helper utilities from local helpers
from messaging_client import get_publisher_client
from messaging_models import build_event_message

def send_to_dead_letter(original_message, failure_reason):
    """Publish the failed message to a dead-letter topic for later analysis.

    Args:
        original_message (dict): The original message payload.
        failure_reason (str): Human‑readable reason for the failure.
    """
    publisher = get_publisher_client()
    dl_payload = {
        'original_payload': original_message,
        'failure_reason': failure_reason,
        'timestamp': '2025-08-27T12:00:00Z'
    }
    message = build_event_message(dl_payload)
    future = publisher.publish(DLQ_TOPIC, message)
    try:
        future.result()
        print(f'Sent to dead-letter topic: {DLQ_TOPIC}')
    except Exception as e:
        print(f'Error publishing dead-letter message: {e}')

def main():
    failed_msg = {'user_id': 'abc', 'action': 'logout', 'error': 'invalid token'}
    send_to_dead_letter(failed_msg, 'Invalid authentication token')

if __name__ == '__main__':
    main()
