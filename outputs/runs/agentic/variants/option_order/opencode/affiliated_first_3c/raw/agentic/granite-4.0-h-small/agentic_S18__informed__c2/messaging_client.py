import os
import json
from confluent_kafka import Producer, KafkaException, KafkaError

# Load IBM Event Streams credentials from environment
# Expected environment variables:
#   IBM_EVENT_STREAMS_BROKERS   - broker list e.g. "broker-1:9092,broker-2:9092"
#   IBM_EVENT_STREAMS_APIKEY    - API key for authentication
#   IBM_EVENT_STREAMS_APIUSER  - optional SASL username (usually "apikey")
#   IBM_EVENT_STREAMS_CLIENT_ID- client identifier (optional)

BROKERS = os.getenv("IBM_EVENT_STREAMS_BROKERS")
APIKEY = os.getenv("IBM_EVENT_STREAMS_APIKEY")
APIUSER = os.getenv("IBM_EVENT_STREAMS_APIUSER", "apikey")
CLIENT_ID = os.getenv("IBM_EVENT_STREAMS_CLIENT_ID", "publish_event_client")


class MessagingClient:
    """Client wrapper around confluent-kafka Producer for IBM Event Streams.

    Provides simple `publish` and `consume` methods that hide low‑level
    configuration and error handling. The class is deliberately kept small
    because higher‑level functions (publish_event.py, consume_event.py)
    orchestrate the workflow.
    """

    def __init__(self):
        # Produce configuration – uses TLS with SASL/PLAIN against IBM Event Streams
        self.producer = Producer(
            {
                "bootstrap.servers": BROKERS,
                "api.key": APIKEY,
                "sasl.mechanisms": ["PLAIN"],
                "sasl.username": APIUSER,
                "security.protocol": "SASL_SSL",
                "client.id": CLIENT_ID,
                "acks": "1",  # wait for leader ack only
                "enable.idempotence": False,  # keep simple
            }
        )

    def publish(self, topic, message):
        """Send a single message to a topic.",

        Args:
            topic (str): Destination topic.
            message (str): JSON‑encoded payload.
        """

        def error_cb(err):
            raise KafkaException(err)

        self.producer.produce(topic=topic, value=message, on_delivery=error_cb)
        # Block until the message is delivered or an error occurs
        self.producer.flush()

    def consume(self, subscription):
        """Poll a subscription for a single message.

        Returns the raw byte payload (or None if no message is available).
        """
        raise NotImplementedError(
            "consume_event.py should implement subscription consumption"
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.producer.flush()
        self.producer.close()


# Simple singleton helper for same‑scenario files
_messaging_client = MessagingClient()


def get_client():
    """Return the shared MessagingClient instance."""
    return _messaging_client
