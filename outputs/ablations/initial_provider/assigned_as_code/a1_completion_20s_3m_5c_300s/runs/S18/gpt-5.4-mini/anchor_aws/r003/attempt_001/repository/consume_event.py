import base64

from google.cloud import pubsub_v1

from messaging_client import load_config, subscriber_client
from messaging_models import normalize_message


def consume_event(config=None):
    config = load_config(config)
    client = subscriber_client(config)
    response = client.pull(subscription=config["subscription_path"], max_messages=1)
    messages = []
    for received in response.received_messages:
        payload = received.message.data
        try:
            payload = base64.b64decode(payload)
        except Exception:
            pass
        messages.append(
            {
                "message_id": received.message.message_id,
                "data": normalize_message(payload),
                "attributes": dict(received.message.attributes),
            }
        )
        client.acknowledge(subscription=config["subscription_path"], ack_ids=[received.ack_id])
    return {"messages": messages}
