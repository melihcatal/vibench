import os
from confluent_kafka import Consumer, KafkaException
from messaging_client import get_kafka_client

# Confluent Kafka (IBM Event Streams / Confluent Cloud)
bootstrap_servers = os.getenv("CONFLUENT_BOOTSTRAP_SERVERS")
api_key = os.getenv("CONFLUENT_API_KEY")


def get_consumer_group(group_id, topic):
    """Create a Kafka consumer for the given group and topic."""
    conf = {
        "bootstrap.servers": bootstrap_servers,
        "group.id": group_id,
        "api.key": api_key,
        "session.timeout.ms": 6000,
    }
    consumer = Consumer(conf)
    consumer.subscribe([topic])
    return consumer


def consume_event(consumer):
    """Poll and return the next message payload (blocking)."""
    try:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            return None
        if msg.error():
            raise KafkaException(msg.error())
        # Return deserialized JSON string as dict
        return msg.value().decode("utf-8")
    except Exception as e:
        print(f"Consumer error: {e}")
        raise


if __name__ == "__main__":
    # Example usage (remove in production)
    consumer = get_consumer_group("my-group", "my_topic")
    while True:
        message = consume_event(consumer)
        if message is not None:
            print(f"Consumed: {message}")
            # Optionally commit after processing
            # consumer.commit(asynchronous=True)
