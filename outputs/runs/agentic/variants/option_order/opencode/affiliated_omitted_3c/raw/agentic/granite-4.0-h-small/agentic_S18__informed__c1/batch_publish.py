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


def publish_batch(topic, messages):
    """Publish a list of JSON messages to a Kafka topic atomically.

    Args:
        topic (str): Kafka topic name.
        messages (list[dict]): List of JSON-serializable messages.
    """
    try:
        # Build a list of (topic, value) tuples
        batch = [(topic, json.dumps(msg).encode("utf-8")) for msg in messages]
        producer.produce(batch=batch)
        producer.flush()
        print(f"Published {len(messages)} messages to {topic}")
    except Exception as e:
        print(f"Batch publish failed: {e}")


if __name__ == "__main__":
    messages = [
        {"id": "batch1", "payload": "first"},
        {"id": "batch2", "payload": "second"},
    ]
    publish_batch("my.batch", messages)
