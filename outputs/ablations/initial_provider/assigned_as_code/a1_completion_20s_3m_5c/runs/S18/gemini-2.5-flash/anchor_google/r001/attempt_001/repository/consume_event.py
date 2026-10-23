import json
import time
from messaging_client import get_subscriber_client, get_subscription_path
from messaging_models import parse_message_payload

def consume_event(config=None):
    config = config or {}
    subscriber = get_subscriber_client()
    subscription_id = config["subscription_id"]
    subscription_path = get_subscription_path(subscriber, subscription_id)

    print(f"Listening for messages on {subscription_path}...")

    message_data = None
    message_id = None
    ack_id = None
    attributes = None

    # Use a callback to process messages
    def callback(message):
        nonlocal message_data, message_id, ack_id, attributes
        message_data = parse_message_payload(message.data)
        message_id = message.message_id
        ack_id = message.ack_id
        attributes = dict(message.attributes)
        print(f"Received message: {message_id}")
        print(f"Data: {message_data}")
        print(f"Attributes: {attributes}")
        message.ack()
        # To stop the flow after receiving one message
        # subscriber.deactivate_flow(subscription_path)

    # The subscriber client is an asynchronous client. We will block until a message is received.
    # In a real application, you might run this in a non-blocking way or as a long-running process.
    future = subscriber.subscribe(subscription_path, callback=callback)
    try:
        # We wait for a message to be processed or timeout
        future.result(timeout=config.get("timeout", 30))
    except Exception as e:
        print(f"No messages received within the timeout or an error occurred: {e}")
        future.cancel()
        subscriber.close()
        return None
    finally:
        subscriber.close()

    if message_id:
        return {
            "message_id": message_id,
            "data": message_data,
            "attributes": attributes,
            "ack_id": ack_id
        }
    else:
        return None
