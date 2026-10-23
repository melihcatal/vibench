import json
from messaging_client import PubSubClient


def send_dead_letter(failed_topic: str, dead_letter_topic: str, message: dict) -> None:
    """Send a failed message to a dead‑letter destination.

    Args:
        failed_topic: Topic where the original message failed.
        dead_letter_topic: Destination topic for dead‑lettering.
        message: The failed message payload (as dict).
    """
    client = PubSubClient()
    dl_message = json.dumps(message)
    client.publish(dead_letter_topic, dl_message)
    print(
        f"Dead‑lettered message to {dead_letter_topic} (originally from {failed_topic})"
    )
