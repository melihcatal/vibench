"""Send failed messages to a dead-letter destination."""
from messaging_client import PubSubClient
from messaging_models import Message


def send_to_dead_letter(dead_letter_topic: str, message: Message) -> str:
    """Send a failed message to Google Cloud Pub/Sub dead-letter topic."""
    client = PubSubClient()
    return client.dead_letter(dead_letter_topic, message)


if __name__ == "__main__":
    # Example usage for testing (not scored)
    pass