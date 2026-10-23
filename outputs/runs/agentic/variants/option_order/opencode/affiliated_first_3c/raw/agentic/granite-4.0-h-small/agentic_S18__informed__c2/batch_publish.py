import json
from messaging_client import MessagingClient


def batch_publish(topic, messages):
    """Publish a batch of messages (max 10) to the configured topic.

    Each message must be a dict with at least an 'id' attribute. The
    MessagingClient (IBM Event Streams) adds any additional attributes
    unchanged and sends the JSON payload securely using the IBM Event Streams
    credentials.

    Parameters:
        topic (str): Target topic name.
        messages (list[dict]): List of message dicts. Must contain an 'id'
                               field; other fields are preserved.
    """
    if not isinstance(messages, list):
        raise ValueError("messages must be a list")
    if len(messages) == 0:
        return  # nothing to publish
    # Ensure each message has a unique ID
    ids = {msg.get("id") for msg in messages}
    if len(ids) != len(messages):
        raise ValueError("All messages must have unique 'id' fields")
    # Convert each dict to JSON string and send
    for msg in messages:
        MessagingClient().publish(topic, json.dumps(msg))


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    batch = [
        {"id": "msg-1", "type": "order_created", "amount": 100},
        {"id": "msg-2", "type": "order_updated", "status": "shipped"},
    ]
    batch_publish("my-orders-topic", batch)
