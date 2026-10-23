import json
import os
from messaging_client import get_pubsub_subscriber_client
from messaging_models import PubSubMessage

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
SUBSCRIPTION_ID = os.environ.get("PUBSUB_SUBSCRIPTION_ID")


def consume_event(timeout: float = 5.0) -> PubSubMessage | None:
    subscriber = get_pubsub_subscriber_client()
    subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)

    response = subscriber.pull(
        request={
            "subscription": subscription_path,
            "max_messages": 1,
            "return_immediately": True,
        }
    )

    if not response.received_messages:
        return None

    received_message = response.received_messages[0]
    message_data = received_message.message.data.decode("utf-8")
    message_attributes = dict(received_message.message.attributes)
    message_id = received_message.message.message_id

    # Acknowledge the message
    ack_ids = [received_message.ack_id]
    subscriber.acknowledge(
        request={"subscription": subscription_path, "ack_ids": ack_ids}
    )

    return PubSubMessage(
        data=json.loads(message_data),
        message_id=message_id,
        attributes=message_attributes,
    )
