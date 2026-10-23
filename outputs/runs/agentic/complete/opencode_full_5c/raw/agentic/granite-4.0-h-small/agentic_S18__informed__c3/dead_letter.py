import os
import json
from confluent_kafka import Producer
from messaging_client import get_kafka_client

# Use the same Confluent Kafka client (IBM Event Streams / Confluent Cloud)
bootstrap_servers = os.getenv("CONFLUENT_BOOTSTRAP_SERVERS")
api_key = os.getenv("CONFLUENT_API_KEY")


def get_dlq_producer(dlq_topic):
    """Create a producer dedicated to the dead-letter topic."""
    producer = get_kafka_client(bootstrap_servers)
    producer.configure({"api.key": api_key})
    return producer


def send_to_dead_letter(original_topic, msg_key, raw_msg, error):
    """
    Send a failed message (as received by the consumer) to a dead-letter topic.

    Args:
        original_topic (str): The topic where the message originally arrived.
        msg_key (str): Kafka message key (if any).
        raw_msg (str): Raw message value.
        error (Exception): Exception that caused the failure.
    """
    dlq_topic = f"{original_topic}-dlq"
    dlq_producer = get_dlq_producer(dlq_topic)
    dlq_payload = {
        "original_topic": original_topic,
        "key": msg_key,
        "message": raw_msg,
        "error": str(error),
        "timestamp": int(os.time()),
    }
    try:
        dlq_producer.produce(
            topic=dlq_topic, key=msg_key, value=json.dumps(dlq_payload)
        )
        dlq_producer.flush()
        print(f"DLQ: Sent to {dlq_topic}")
    except Exception as e:
        print(f"DLQ submit failed: {e}")


if __name__ == "__main__":
    # Example (for testing)
    send_to_dead_letter(
        original_topic="my_topic",
        msg_key="key1",
        raw_msg='{"data":"example"}',
        error=RuntimeError("Processing error"),
    )
