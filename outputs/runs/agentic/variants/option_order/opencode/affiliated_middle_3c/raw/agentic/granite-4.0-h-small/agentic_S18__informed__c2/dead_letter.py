import os
from messaging_client import PubSubClient


def send_to_dead_letter(failed_message, dead_letter_topic):
    """Send a failed message to a dead-letter topic/queue.

    Args:
        failed_message (dict): The original message payload.
        dead_letter_topic (str): Destination dead-letter topic name.
    """
    client = PubSubClient()
    payload = json.dumps(failed_message)
    # Publish to dead-letter destination (Google Cloud Pub/Sub example)
    client.publish(dead_letter_topic, payload)
    print(f"Sent failed message to dead-letter topic {dead_letter_topic}")


if __name__ == "__main__":
    # Example usage with environment variables
    dead_letter_topic = os.getenv("DEAD_LETTER_TOPIC")
    if not dead_letter_topic:
        raise RuntimeError("DEAD_LETTER_TOPIC environment variable not set")
    # Simulated failed message fetched from elsewhere in your code
    failed_message = {
        "id": "failed_001",
        "error": "Parsing error",
        "original": {"msg": "Hello"},
    }
    send_to_dead_letter(failed_message, dead_letter_topic)
