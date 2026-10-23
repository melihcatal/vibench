import json
from typing import List, Dict, Any

from .messaging_client import MessagingClient
from .messaging_models import PubSubMessage


def dead_letter(message: Dict[str, Any], dlq_topic: str, reason: str = "") -> None:
    """Send a failed Pub/Sub message to a dead-letter topic using a concrete provider.
    This uses Google Cloud Pub/Sub SDK. Credentials are provided via
    GOOGLE_APPLICATION_CREDENTIALS environment variable.
    """
    client = MessagingClient()
    dlq_message = PubSubMessage(
        data=json.dumps(message).encode("utf-8"), attributes={"reason": reason}
    )
    client.publish(dlq_topic, dlq_message)


# Additional helper to send a batch of failed messages


def dead_letter_batch(
    failed_messages: List[Dict[str, Any]], dlq_topic: str, reason: str = ""
) -> None:
    client = MessagingClient()
    for msg in failed_messages:
        dlq_message = PubSubMessage(
            data=json.dumps(msg).encode("utf-8"), attributes={"reason": reason}
        )
        client.publish(dlq_topic, dlq_message)
