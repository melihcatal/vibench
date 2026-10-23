import json
import os
from confluent_kafka import Consumer, KafkaError

# Configure IBM Event Streams / Confluent Kafka broker details
BOOTSTRAP_SERVERS = os.getenv("IBM_EVENT_STREAMS_BROKERS")
API_KEY = os.getenv("IBM_EVENT_STREAMS_APIKEY")

# Topic to subscribe to and group for consumer
TOPIC = "my-events"
GROUP_ID = "my-consumer-group"

# Create a Kafka consumer instance
consumer = Consumer(
    {
        "bootstrap.servers": BOOTSTRAP_SERVERS,
        "api.key": API_KEY,
        "group.id": GROUP_ID,
        "auto.offset.reset": "earliest",
    }
)


def consume_event(num_messages=1):
    """Consume one or more messages from the topic.

    Args:
        num_messages (int): Number of messages to fetch (default is 1).
    """
    try:
        consumer.subscribe([TOPIC])
        for _ in range(num_messages):
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event (expected)
                    continue
                else:
                    print(f"Error while consuming: {msg.error()}")
                    break
            # Decode JSON payload
            payload = json.loads(msg.value().decode("utf-8"))
            print(f"Consumed message: {payload}")
            # Commit the offset after successful processing
            consumer.commit(asynchronous=False)
    finally:
        consumer.close()


# Example usage
if __name__ == "__main__":
    consume_event(num_messages=1)
