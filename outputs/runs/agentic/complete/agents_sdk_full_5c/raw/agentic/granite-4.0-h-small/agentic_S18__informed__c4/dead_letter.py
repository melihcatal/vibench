import os
from google.cloud import pubsub_v1
from messaging_client import get_publisher_client
from messaging_models import prepare_dead_letter

project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
dead_letter_topic = os.getenv('DEAD_LETTER_TOPIC', 'dead-letter-topic')

def send_dead_letter(original_message, error_details):
    """Send a failed message to a dead-letter Pub/Sub topic.

    Args:
        original_message (dict): Original message payload that caused error.
        error_details (str): Human‑readable description of the failure.
    """
    dl_payload = prepare_dead_letter(original_message, error_details)
    publisher = get_publisher_client()
    data = str(dl_payload).encode('utf-8')
    publisher.publish(dead_letter_topic, data=data)
    print(f"Dead‑lettered message with details: {error_details}")
