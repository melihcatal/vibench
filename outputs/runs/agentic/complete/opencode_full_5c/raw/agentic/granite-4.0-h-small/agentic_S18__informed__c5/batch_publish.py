import json
from typing import List, Dict, Any

from .messaging_client import MessagingClient
from .messaging_models import PubSubMessage


def batch_publish(
    topic_name: str, events: List[Dict[str, Any]], batch_id: str
) -> List[str]:
    """Publish a batch of JSON events to a Pub/Sub topic with per‑event attributes.
    This uses Google Cloud Pub/Sub SDK. Credentials are provided via
    GOOGLE_APPLICATION_CREDENTIALS environment variable.
    Returns a list of message IDs.
    """
    client = MessagingClient()
    messages = []
    for idx, ev in enumerate(events):
        # Include a per‑event attribute to illustrate batch processing
        ev["batch_id"] = batch_id
        ev["event_id"] = idx
        message = PubSubMessage(
            data=json.dumps(ev).encode("utf-8"), attributes={"batch": batch_id}
        )
        messages.append(message)
    # Publish all messages in one call (provider‑specific)
    message_ids = client.publish_batch(topic_name, messages)
    return message_ids
