import os
from confluent_kafka import Consumer, KafkaError

cfg = {
    "bootstrap.servers": os.getenv("CONFLUENT_BOOTSTRAP_SERVERS"),
    "group.id": os.getenv("CONSUMER_GROUP", "default-consumer"),
    "auto.offset.reset": "earliest",
    "api.key": os.getenv("CONFLUENT_API_KEY"),
}
consumer = Consumer(cfg)
consumer.subscribe([os.getenv("CONSUME_TOPIC")])


def consume_event():
    """Consume a single message from the configured topic and return its payload.

    Returns:
        dict: Deserialized JSON payload of the consumed message.
    """
    msg = consumer.poll(timeout=1.0)
    if msg is None:
        return None
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            return None
        else:
            raise KafkaError(msg.error())
    return json.loads(msg.value())
