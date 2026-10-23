import json
import os
from confluent_kafka import Producer

# Configure IBM Event Streams / Confluent Kafka broker details
BOOTSTRAP_SERVERS = os.getenv("IBM_EVENT_STREAMS_BROKERS")
API_KEY = os.getenv("IBM_EVENT_STREAMS_APIKEY")

# Topic where batch messages will be published
TOPIC = "my-events"

# Create a Kafka producer instance
producer = Producer(
    {
        "bootstrap.servers": BOOTSTRAP_SERVERS,
        "api.key": API_KEY,
    }
)


def publish_batch(events):
    """Publish a list of JSON events to the topic.

    Args:
        events (list[dict]): Each dict represents an event to send.
    """
    try:
        for event in events:
            message = json.dumps(event).encode("utf-8")
            producer.produce(TOPIC, message)
        producer.flush()
        print(f"Batch published: {len(events)} events")
    except Exception as e:
        print(f"Batch publish failed: {e}")


# Example usage
if __name__ == "__main__":
    batch = [
        {"id": "b1", "action": "order_created", "amount": 45.0},
        {"id": "b2", "action": "order_created", "amount": 120.5},
        {"id": "b3", "action": "order_created", "amount": 30.0},
    ]
    publish_batch(batch)
