import json
import os
from confluent_kafka import Producer

# Configure IBM Event Streams / Confluent Kafka broker details for dead-letter topic
BOOTSTRAP_SERVERS = os.getenv("IBM_EVENT_STREAMS_BROKERS")
API_KEY = os.getenv("IBM_EVENT_STREAMS_APIKEY")

# Dead-letter topic name
DL_TOPIC = "my-dead-letter"

# Create a Kafka producer instance for DL
producer = Producer(
    {
        "bootstrap.servers": BOOTSTRAP_SERVERS,
        "api.key": API_KEY,
    }
)


def send_to_dead_letter(original_event, error):
    """Send a failed event to the dead-letter topic along with error details.

    Args:
        original_event (dict): The original event that could not be processed.
        error (Exception or str): Description of the failure.
    """
    try:
        dl_payload = {
            "original_event": original_event,
            "error": str(error),
            "timestamp": __import__("datetime").datetime.utcnow().isoformat(),
        }
        dl_message = json.dumps(dl_payload).encode("utf-8")
        producer.produce(DL_TOPIC, dl_message)
        producer.flush()
        print(f"Sent to dead-letter: {dl_payload}")
    except Exception as e:
        print(f"Failed to deliver to dead-letter topic: {e}")


# Example usage (would normally be invoked on processing errors)
if __name__ == "__main__":
    failed_event = {"id": "evt-999", "action": "order_failed"}
    send_to_dead_letter(failed_event, "Simulated processing error")
