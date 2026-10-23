# batch_publish.py
import os
import json
from confluent_kafka import Producer, KafkaError

# Confluent Cloud Kafka configuration variables (set in environment)
BOOTSTRAP_SERVERS = os.getenv("CONFLUENT_BOOTSTRAP_SERVERS")
API_KEY = os.getenv("CONFLUENT_API_KEY")

producer = Producer(
    {
        "bootstrap.servers": BOOTSTRAP_SERVERS,
        "api.key": API_KEY,
    }
)


def publish_batch(topic, events):
    """Publish a list of event dictionaries to a Kafka topic in a single batch.
    :param events: List of dicts, each representing an event payload.
    """
    if not events:
        print("No events to publish.")
        return
    try:
        messages = []
        for ev in events:
            messages.append(json.dumps(ev).encode("utf-8"))
        # Producer's produce() supports sending a list of (topic, value) tuples
        producer.produce(topic=topic, value=messages)
        producer.flush()
        print(f"Batch of {len(events)} events published to {topic}.")
    except Exception as e:
        print(f"Batch publish failed: {e}")


if __name__ == "__main__":
    # Example batch (remove/replace with your own usage)
    sample_batch = [
        {"id": "batch-1", "data": {"value": 1}},
        {"id": "batch-2", "data": {"value": 2}},
        {"id": "batch-3", "data": {"value": 3}},
    ]
    publish_batch("my-events", sample_batch)
