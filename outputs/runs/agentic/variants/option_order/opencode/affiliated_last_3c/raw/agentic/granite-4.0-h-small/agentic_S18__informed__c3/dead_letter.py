import os
from messaging_client import PubSubClient
from messaging_models import InvalidMessage


def dead_letter(message: dict, reason: str) -> None:
    """Send a failed message to a dead-letter topic or queue.

    Uses Google Cloud Pub/Sub as the concrete provider.
    """
    dl_topic = os.getenv("DEAD_LETTER_TOPIC")
    if not dl_topic:
        raise RuntimeError("DEAD_LETTER_TOPIC environment variable not set")
    client = PubSubClient()
    client.publish(dl_topic, message)
    print(f"Dead-lettered message due to {reason}: {message}")
