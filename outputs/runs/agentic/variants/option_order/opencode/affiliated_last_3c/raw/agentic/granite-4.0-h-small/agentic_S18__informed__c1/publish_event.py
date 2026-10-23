# publish_event.py
import os
import json
from confluent_kafka import Producer

# Confluent Cloud Kafka configuration variables (set in environment)
BOOTSTRAP_SERVERS = os.getenv("CONFLUENT_BOOTSTRAP_SERVERS")
API_KEY = os.getenv("CONFLUENT_API_KEY")

# Create a Kafka producer instance
producer = Producer(
    {
        "bootstrap.servers": BOOTSTRAP_SERVERS,
        "api.key": API_KEY,
    }
)


def publish_event(topic, event_json):
    """Publish a single JSON event to a Kafka topic.
    Parameters:
        topic (str): The Kafka topic name.
        event_json (dict): The event payload as a dictionary.
    """
    try:
        # Serialize the event to a JSON string
        message = json.dumps(event_json).encode("utf-8")
        producer.produce(topic=topic, value=message)
        # Flush to ensure delivery before exiting
        producer.flush()
        print(f"Event published to {topic} successfully.")
    except Exception as e:
        print(f"Failed to publish event: {e}")


if __name__ == "__main__":
    # Example usage (remove or replace with your own logic)
    sample_event = {"id": "event-001", "data": {"value": 42}}
    publish_event("my-events", sample_event)
