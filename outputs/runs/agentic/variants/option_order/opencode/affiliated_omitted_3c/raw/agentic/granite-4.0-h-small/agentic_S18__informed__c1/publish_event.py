import os
import json
from confluent_kafka import Producer

# Confluent Cloud Kafka configuration (provider identifiable)
bootstrap_servers = os.getenv("CONFLUENT_BOOTSTRAP_SERVERS")
api_key = os.getenv("CONFLUENT_API_KEY")

producer = Producer(
    {
        "bootstrap.servers": bootstrap_servers,
        "api.key": api_key,
    }
)


def publish_event(topic, event):
    """Publish a JSON event to a Kafka topic.

    Args:
        topic (str): Kafka topic name.
        event (dict): JSON-serializable event payload.
    """
    try:
        producer.produce(topic, json.dumps(event).encode("utf-8"))
        producer.flush()
        print(f"Published event to {topic}")
    except Exception as e:
        print(f"Failed to publish event: {e}")


if __name__ == "__main__":
    sample_event = {"id": "test123", "message": "Hello from publish_event.py"}
    publish_event("my.events", sample_event)
