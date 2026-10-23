import os
from confluent_kafka import Producer, Consumer, KafkaError


def get_producer():
    """Return a Kafka producer configured for IBM Event Streams / Confluent Cloud."""
    conf = {
        "bootstrap.servers": os.getenv("CONFLUENT_BOOTSTRAP_SERVERS"),
        "api.key": os.getenv("CONFLUENT_API_KEY"),
    }
    return Producer(conf)


def get_consumer(group_id=None):
    """Return a Kafka consumer for consuming from a topic."""
    cfg = {
        "bootstrap.servers": os.getenv("CONFLUENT_BOOTSTRAP_SERVERS"),
        "group.id": group_id or "default-group",
        "auto.offset.reset": "earliest",
        "api.key": os.getenv("CONFLUENT_API_KEY"),
    }
    return Consumer(cfg)


def publish(producer, topic, key, value):
    """Publish a single JSON message."""
    producer.produce(
        topic=topic, key=key, value=value.encode("utf-8"), on_delivery=handle_delivery
    )
    producer.flush()


def handle_delivery(err, msg):
    if err:
        print(f"Publish error: {err}")
    else:
        print(f"Message delivered to {msg.topic()}[{msg.partition()}] key={msg.key()}")


def consume_once(consumer, topic):
    """Poll a single message from the consumer."""
    msg = consumer.poll(timeout=1.0)
    if msg is None:
        return None
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            return None
        raise KafkaError(msg.error())
    return json.loads(msg.value())
