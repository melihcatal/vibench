import json
from typing import Dict, Any

from .messaging_client import MessagingClient
from .messaging_models import PubSubMessage


def publish_event(topic_name: str, event: Dict[str, Any]) -> str:
    """Publish a JSON event to a Pub/Sub topic using a concrete provider.
    This uses Google Cloud Pub/Sub SDK. Credentials are provided via
    GOOGLE_APPLICATION_CREDENTIALS environment variable.
    Returns the message ID.
    """
    client = MessagingClient()
    message = PubSubMessage(data=json.dumps(event).encode("utf-8"))
    # The id() method returns the provider‑specific message ID after publish
    message_id = client.publish(topic_name, message)
    return message_id
