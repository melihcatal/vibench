# messaging_client.py
import os
from confluent_kafka import Producer, Consumer, KafkaError

# Environment variables for Confluent Cloud Kafka
BOOTSTRAP_SERVERS = os.getenv("CONFLUENT_BOOTSTRAP_SERVERS")
API_KEY = os.getenv("CONFLUENT_API_KEY")
GROUP_ID = os.getenv("CONFLUENT_GROUP_ID", "event-consumer")

# Reusable producer instance
producer = Producer(
    {
        "bootstrap.servers": BOOTSTRAP_SERVERS,
        "api.key": API_KEY,
    }
)

# Reusable consumer instance
consumer = Consumer(
    {
        "bootstrap.servers": BOOTSTRAP_SERVERS,
        "group.id": GROUP_ID,
        "session.timeout.ms": 6000,
        "auto.offset.reset": "earliest",
        "api.key": API_KEY,
    }
)


def init_publisher(topic):
    """Prepare a producer for a specific topic."""
    # No extra topic config needed for basic usage
    return producer


def init_consumer(subscription):
    """Prepare a consumer for a specific topic (subscription)."""
    consumer.subscribe([subscription])
    return consumer


def publish_single(topic, payload):
    """Publish a single JSON payload to a topic."""
    try:
        message = json.dumps(payload).encode("utf-8")
        producer.produce(topic=topic, value=message)
        producer.flush()
        print(f"Published to {topic}")
    except Exception as e:
        print(f"Publish error: {e}")


def consume_single():
    """Consume a single message and return its parsed payload."""
    msg = consumer.poll(timeout=1.0)
    if msg is None:
        print("No message received")
        return None
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            print("Reached end of topic")
        else:
            print(f"Consumer error: {msg.error()}")
        return None
    payload = json.loads(msg.value().decode("utf-8"))
    return payload


def shutdown():
    producer.flush()
    consumer.close()


# Note: In production you would typically import these utilities rather than keep them in a helper module.
