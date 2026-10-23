import os
import json
from confluent_kafka import Producer

# Confluent Cloud Kafka configuration (provider identifiable)
bootstrap_servers = os.getenv("CONFLUENT_BOOTSTRAP_SERVERS")
api_key = os.getenv("CONFLUENT_API_KEY")

dead_letter_topic = "my.deadletter"

producer = Producer(
    {
        "bootstrap.servers": bootstrap_servers,
        "api.key": api_key,
    }
)


def send_dead_letter(original_topic, message, error):
    """Send a failed message to a dead-letter topic with failure metadata.

    Args:
        original_topic (str): The topic where delivery failed.
        message (dict): The original message payload.
        error (Exception): Exception raised during processing.
    """
    dl_payload = {
        "original_topic": original_topic,
        "message": message,
        "error": str(error),
    }
    try:
        producer.produce(dead_letter_topic, json.dumps(dl_payload).encode("utf-8"))
        producer.flush()
        print(f"Sent dead letter for {original_topic}: {error}")
    except Exception as e:
        print(f"Failed to send dead letter: {e}")


if __name__ == "__main__":
    sample_msg = {"id": "dl-test", "content": "This is a dead letter message"}
    send_dead_letter("my.events", sample_msg, ValueError("publish failed"))
