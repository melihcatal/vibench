from google.cloud import pubsub_v1

from messaging_client import get_config, subscriber_client


def consume_event(config=None):
    config = get_config(config)
    client = subscriber_client()
    subscription = client.subscription_path(config["project_id"], config["subscription_id"])
    response = client.pull(subscription=subscription, max_messages=1, timeout=30)
    messages = response.received_messages
    if not messages:
        client.close()
        return {"message": None}
    received = messages[0]
    client.acknowledge(subscription=subscription, ack_ids=[received.ack_id])
    client.close()
    return {"message_id": received.message.message_id, "data": received.message.data.decode("utf-8"), "attributes": dict(received.message.attributes)}
