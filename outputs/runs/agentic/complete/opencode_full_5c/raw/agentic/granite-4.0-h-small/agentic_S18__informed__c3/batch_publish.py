import os
import json
from confluent_kafka import Producer
from messaging_client import get_kafka_client

# Confluent Kafka (IBM Event Streams / Confluent Cloud)
bootstrap_servers = os.getenv("CONFLUENT_BOOTSTRAP_SERVERS")
api_key = os.getenv("CONFLUENT_API_KEY")

producer = get_kafka_client(bootstrap_servers)
producer.configure({"api.key": api_key})


def batch_publish(topic, messages):
    """
    Publish a list of messages (each a dict) to the given topic.
    Messages are sent in a single produce batch with optional keys/headers.

    Args:
        topic (str): Target topic.
        messages (List[dict]): List of message payloads to publish.
    """
    try:
        # Confluent Kafka ParallelProducer is suitable for true batching
        for msg in messages:
            # Using key to keep ordering per key
            key = msg.get("id")
            producer.produce(topic=topic, key=key, value=json.dumps(msg))
        producer.flush()
        print(f"Batch of {len(messages)} messages sent to {topic}")
    except Exception as e:
        print(f"Batch publish failed: {e}")


if __name__ == "__main__":
    # Example usage
    msg_list = [
        {"id": "1", "payload": {"msg": "first"}},
        {"id": "2", "payload": {"msg": "second"}},
        {"id": "3", "payload": {"msg": "third"}},
    ]
    batch_publish("my_topic", msg_list)
