import os
import json
from confluent_kafka import Consumer, KafkaException

# Confluent Cloud Kafka configuration (provider identifiable)
bootstrap_servers = os.getenv("CONFLUENT_BOOTSTRAP_SERVERS")
api_key = os.getenv("CONFLUENT_API_KEY")

c = Consumer(
    {
        "bootstrap.servers": bootstrap_servers,
        "api.key": api_key,
        "group.id": "my-consumer-group",
        "auto.offset.reset": "earliest",
    }
)


def consume_message(topic, partition=0):
    """Consume one message from a Kafka topic.

    Args:
        topic (str): Kafka topic name.
        partition (int): Partition to read from (default 0).
    """
    try:
        c.assign([TopicPartition(topic, partition)])
        msg = c.poll(timeout=1.0)
        if msg is None:
            print("No message received")
            return None
        if msg.error():
            raise KafkaException(msg.error())
        payload = json.loads(msg.value().decode("utf-8"))
        print(f"Consumed message: {payload} from {topic}")
        return payload
    except Exception as e:
        print(f"Error consuming message: {e}")
        return None


if __name__ == "__main__":
    msg = consume_message("my.events")
