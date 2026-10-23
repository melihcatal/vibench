import json
from messaging_client import MessagingClient


def publish_event(topic, payload):
    """Publish a JSON event to the configured Pub/Sub topic.

    Uses the default MessagingClient (configured for IBM Event Streams)
    which sends messages securely using IBM_EVENT_STREAMS_BROKERS and
    IBM_EVENT_STREAMS_APIKEY.

    Args:
        topic (str): The messaging topic name.
        payload (dict): The event data to publish.
    """
    # Convert payload to JSON string
    message = json.dumps(payload)
    # Use the same-scenario client helper
    MessagingClient().publish(topic, message)


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    event = {
        "event_id": "e-12345",
        "type": "order_created",
        "timestamp": "2025-08-15T12:34:56Z",
        "data": {"order_id": "ORD-001", "amount": 199.99},
    }
    publish_event("my-orders-topic", event)
