import os
import json
from google.cloud import pubsub_v1

PROJECT_ID = os.environ.get("GOOGLE_PROJECT_ID", "default-project")
SUBSCRIPTION_ID = os.environ.get("GOOGLE_PUBSUB_SUBSCRIPTION_ID", "events-subscription")

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)


def consume_event(ack: bool = True) -> dict | None:
    response = subscriber.pull(
        request={"subscription": subscription_path, "max_messages": 1}
    )
    if not response.received_messages:
        return None
    msg = response.received_messages[0].message
    data = json.loads(msg.data.decode("utf-8"))
    attributes = dict(msg.attributes)
    if ack:
        ack_id = response.received_messages[0].ack_id
        subscriber.acknowledge(
            request={"subscription": subscription_path, "ack_ids": [ack_id]}
        )
    return {
        "message_id": msg.message_id,
        "data": data,
        "attributes": attributes,
    }
