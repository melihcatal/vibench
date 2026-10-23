import json
import os
from confluent_kafka import Producer

# Configure IBM Event Streams / Confluent Kafka broker details
BOOTSTRAP_SERVERS = os.getenv("IBM_EVENT_STREAMS_BROKERS")
API_KEY = os.getenv("IBM_EVENT_STREAMS_APIKEY")

# Topic where events will be published
TOPIC = "my-events"

# Create a Kafka producer instance
producer = Producer(
    {
        "bootstrap.servers": BOOTSTRAP_SERVERS,
        "api.key": API_KEY,
    }
)


def publish_event(event_payload):
    """Publish a JSON event to the configured topic.

    Args:
        event_payload (dict): The event data to publish.
    """
    try:
        # Serialize the event as JSON
        message = json.dumps(event_payload).encode("utf-8")
        # Deliver (synchronously) the message
        producer.produce(TOPIC, message)
        producer.flush()
        print(f"Published event: {event_payload}")
    except Exception as e:
        print(f"Failed to publish event: {e}")


# Example usage
if __name__ == "__main__":
    sample_event = {
        "id": "evt-001",
        "action": "order_created",
        "details": {"order_id": "12345", "amount": 99.99},
    }
    publish_event(sample_event)
