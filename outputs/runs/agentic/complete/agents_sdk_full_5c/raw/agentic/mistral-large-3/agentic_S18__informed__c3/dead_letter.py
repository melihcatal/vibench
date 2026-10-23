# Sends failed messages to Google Cloud Pub/Sub dead-letter topic
from messaging_client import PubSubClient
from messaging_models import DeadLetterRequest, PubSubMessage
import os


def send_to_dead_letter(failed_message: PubSubMessage, error_details: dict, dead_letter_topic: str) -> str:
    """Send a failed message to the dead-letter topic in Google Cloud Pub/Sub."""
    client = PubSubClient()
    request = DeadLetterRequest(
        failed_message=failed_message,
        error_details=error_details,
        dead_letter_topic=dead_letter_topic
    )
    message_id = client.dead_letter_message(request)
    return message_id