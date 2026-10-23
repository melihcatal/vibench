import os
from confluent_kafka import Producer, Consumer, KafkaException

# Confluent Cloud Kafka configuration (provider identifiable)
bootstrap_servers = os.getenv("CONFLUENT_BOOTSTRAP_SERVERS")
api_key = os.getenv("CONFLUENT_API_KEY")

# Shared producer and consumer instances
producer = Producer(
    {
        "bootstrap.servers": bootstrap_servers,
        "api.key": api_key,
    }
)

consumer = Consumer(
    {
        "bootstrap.servers": bootstrap_servers,
        "api.key": api_key,
        "group.id": os.getenv("CONFLUENT_CONSUMER_GROUP", "default-consumer-group"),
        "auto.offset.reset": "earliest",
    }
)


def get_producer():
    """Return the configured Kafka producer."""
    return producer


def get_consumer():
    """Return the configured Kafka consumer."""
    return consumer


if __name__ == "__main__":
    # Simple test: produce and then consume a message
    msg = {"id": "client-test", "msg": "Hello from messaging_client"}
    producer.produce("my.test", json.dumps(msg).encode("utf-8"))
    producer.flush()
    consumer.assign([TopicPartition("my.test", 0)])
    while True:
        ev = consumer.poll(timeout=1.0)
        if ev is None:
            break
        if ev.error():
            raise KafkaException(ev.error())
        print("Received message:", json.loads(ev.value()))
