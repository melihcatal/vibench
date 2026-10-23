import os
import json
from concurrent.futures import TimeoutError
from messaging_client import PubSubClient
from messaging_models import PubSubMessage

# Google Cloud Pub/Sub provider-specific signal

def consume_event(subscription_id: str, timeout: float = 5.0) -> PubSubMessage:
    client = PubSubClient()
    subscriber = client.get_subscriber_client()
    subscription_path = client.get_subscription_path(subscription_id)

    pulled_message = None

    def callback(message):
        nonlocal pulled_message
        pulled_message = PubSubMessage.from_json(
            message.data.decode("utf-8"),
            message_id=message.message_id,
            attributes=dict(message.attributes)
        )
        message.ack() # Acknowledge the message to remove it from the subscription

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}...")

    try:
        streaming_pull_future.result(timeout=timeout)
    except TimeoutError:
        streaming_pull_future.cancel()  # Trigger the shutdown.
        streaming_pull_future.result()  # Block until the shutdown is complete.
    except Exception as e:
        streaming_pull_future.cancel()  # Trigger the shutdown.
        streaming_pull_future.result()  # Block until the shutdown is complete.
        raise e

    return pulled_message
