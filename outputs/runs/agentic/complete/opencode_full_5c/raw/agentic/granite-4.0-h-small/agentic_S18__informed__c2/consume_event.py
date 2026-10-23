import json
from messaging_client import get_messaging_client


def consume_event(subscription, max_messages=1, wait_seconds=10):
    """Consume up to max_messages from a managed subscription.

    Uses IBM Event Streams (Kafka) via the confluent-kafka SDK.
    Required environment variables:
        IBM_EVENT_STREAMS_BROKERS
        IBM_EVENT_STREAMS_APIKEY
    Returns a list of messages (each message is a dict with 'key', 'value', 'headers').
    """
    client = get_messaging_client()
    # Get a consumer for the specified subscription (topic/queue name)
    consumer = client.get_consumer(
        group_id=subscription,
        bootstrap_servers=client.config["bootstrap_servers"],
        api_key=client.config["api_key"],
    )
    # Poll messages from the subscription
    messages = []
    for _ in range(max_messages):
        msg = consumer.poll(timeout=wait_seconds)
        if msg is None or msg.error():
            break
        # Decode JSON payload
        payload = json.loads(msg.value().decode("utf-8"))
        messages.append(
            {"key": msg.key(), "payload": payload, "headers": msg.headers()}
        )
    # Commit offsets after successful consumption
    consumer.commit(asynchronous=False)
    return messages
