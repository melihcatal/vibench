import json
from google.cloud import pubsub_v1
from messaging_client import get_pubsub_config, get_subscriber
from messaging_models import ConsumeResponse, normalize_message


def consume_event(subscription_path=None, timeout=10.0):
    config = get_pubsub_config()
    subscriber = get_subscriber(config)
    subscription_path = subscription_path or config.subscription_path
    response = subscriber.pull(subscription=subscription_path, max_messages=1, timeout=timeout)
    messages = [normalize_message(msg) for msg in response.received_messages]
    return ConsumeResponse(messages=messages, subscription_path=subscription_path).as_dict()
