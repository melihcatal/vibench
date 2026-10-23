# consume_event.py
import os
import json
from confluent_kafka import Consumer, KafkaError

# Confluent Cloud Kafka configuration variables (set in environment)
BOOTSTRAP_SERVERS = os.getenv("CONFLUENT_BOOTSTRAP_SERVERS")
API_KEY = os.getenv("CONFLUENT_API_KEY")
GROUP_ID = os.getenv("CONFLUENT_GROUP_ID", "event-consumer")

consumer = Consumer(
    {
        "bootstrap.servers": BOOTSTRAP_SERVERS,
        "group.id": GROUP_ID,
        "session.timeout.ms": 6000,
        "auto.offset.reset": "earliest",
        "api.key": API_KEY,
    }
)

consumer.subscribe(["my-events"])  # topic to consume from


def consume_event():
    """Consume a single message from the subscription/topic."""
    try:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            print("No message received within timeout.")
            return None
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print("End of partition reached")
            else:
                print(f"Error while consuming: {msg.error()}")
            return None
        # Deserialize JSON payload
        payload = json.loads(msg.value().decode("utf-8"))
        print(f"Consumed event: {payload}")
        return payload
    except Exception as e:
        print(f"Error consuming event: {e}")
        return None


if __name__ == "__main__":
    # Example consumption (remove or replace with your own loop)
    while True:
        event = consume_event()
        if event is not None:
            # Process event here, e.g., send to dead-letter if validation fails
            pass
