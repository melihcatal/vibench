# dead_letter.py
import json
import os
from confluent_kafka import Producer, KafkaError

# Confluent Cloud Kafka configuration variables (set in environment)
BOOTSTRAP_SERVERS = os.getenv("CONFLUENT_BOOTSTRAP_SERVERS")
API_KEY = os.getenv("CONFLUENT_API_KEY")
DLQ_TOPIC = os.getenv("DEAD_LETTER_TOPIC", "failed-events")

producer = Producer(
    {
        "bootstrap.servers": BOOTSTRAP_SERVERS,
        "api.key": API_KEY,
    }
)


def send_to_dead_letter(original_topic, message, error_reason):
    """Send a failed event to a dead-letter Kafka topic."""
    try:
        dl_payload = {
            "original_topic": original_topic,
            "message": message,
            "error_reason": error_reason,
            "timestamp": int(time.time()),
        }
        producer.produce(topic=DLQ_TOPIC, value=json.dumps(dl_payload).encode("utf-8"))
        producer.flush()
        print(f"Dead-lettered message from {original_topic}: {error_reason}")
    except Exception as e:
        print(f"Failed to deliver to dead-letter topic: {e}")


# Ensure required env vars are present (skip actual send for demo)
if __name__ == "__main__":
    import time

    test_message = {"id": "dl-test-001", "data": {"value": "error"}}
    send_to_dead_letter("my-events", test_message, "validation_failed")
