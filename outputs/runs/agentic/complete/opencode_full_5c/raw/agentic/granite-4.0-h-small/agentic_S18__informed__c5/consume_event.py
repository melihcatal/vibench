import json
from typing import List, Dict, Any, Optional

from .messaging_client import MessagingClient
from .messaging_models import PubSubMessage


def consume_event(subscription_name: str) -> Optional[Dict[str, Any]]:
    """Consume a single Pub/Sub message from a subscription using a concrete provider.
    This uses Google Cloud Pub/Sub SDK. Credentials are provided via
    GOOGLE_APPLICATION_CREDENTIALS environment variable.
    Returns the message payload as a dict or None if no message is available.
    """
    client = MessagingClient()
    message = client.consume(subscription_name)
    if not message:
        return None
    # Decode the payload and parse JSON
    payload = json.loads(message.data.decode("utf-8"))
    return payload
