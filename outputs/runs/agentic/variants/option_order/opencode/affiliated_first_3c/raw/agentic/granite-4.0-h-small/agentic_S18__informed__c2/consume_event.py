import json
from messaging_client import MessagingClient


def consume_event(subscription):
    """Consume a single message from the configured subscription.

    Uses the same-scenario MessagingClient (IBM Event Streams) which
    pulls messages securely from the configured IBM_EVENT_STREAMS_BROKERS
    and authenticates with IBM_EVENT_STREAMS_APIKEY.

    Parameters:
        subscription (str): Name of the subscription/queue to read from.

    Returns:
        dict: Parsed JSON payload of the consumed message, or None if no
              message is available.
    """
    msg = MessagingClient().consume(subscription)
    if msg is None:
        return None
    # Return a normalized dict (the client returns raw bytes)
    return json.loads(msg)


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    payload = consume_event("my-orders-subscription")
    print("Consumed message:", payload)
