import os
import json
from messaging_client import PubSubClient


def publish_event(topic_name, event_data):
    """Publish a JSON event to the specified Pub/Sub topic.

    Args:
        topic_name (str): Name of the Pub/Sub topic.
        event_data (dict): Event payload as a dictionary.
    """
    client = PubSubClient()
    # Convert dictionary to JSON string
    payload = json.dumps(event_data)
    # Publish using provider-specific client (Google Cloud Pub/Sub example)
    response = client.publish(topic_name, payload)
    print(f"Published event to {topic_name}: {response}")


if __name__ == "__main__":
    # Example usage with environment variables for topic and payload
    topic = os.getenv("PUBSUB_TOPIC")
    if not topic:
        raise RuntimeError("PUBSUB_TOPIC environment variable not set")
    sample_event = {"id": "evt_001", "message": "Hello Pub/Sub"}
    publish_event(topic, sample_event)
