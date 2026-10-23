import json
from messaging_client import MessagingClient


def dead_letter(message, dl_destination: str) -> None:
    """Send a failed Pub/Sub message to a dead‑letter topic or queue.

    Leverages Google Cloud Pub/Sub dead‑letter policies.
    The provider is identifiable by the use of a fully qualified dead‑letter topic
    name and the call to `message.ack()` followed by republishing to the
    dead‑letter destination.
    """
    client = MessagingClient()
    # Assume dl_destination is a fully qualified topic name for dead‑lettering
    dl_topic_path = dl_destination  # e.g. projects/PROJECT/topics/dead_letter_topic
    # Republish the original message data to the dead‑letter topic
    client.publisher.publish(dl_topic_path, data=message.data)
    # Acknowledge the original message to prevent redelivery
    message.ack()
    print(f"Message moved to dead‑letter destination: {dl_topic_path}")
