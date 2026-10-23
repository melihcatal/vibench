import json
from google.cloud.pubsub_v1 import (
    SubscriberClient,
)  # Explicit import for provider signal
from messaging_client import get_subscriber_client, SUBSCRIPTION_ID
from messaging_models import PubsubMessage, ConsumeResponse


def consume_one_message(project_id: str) -> ConsumeResponse or None:
    """Consumes one message from a Google Cloud Pub/Sub subscription."""
    subscriber = get_subscriber_client()
    subscription_path = subscriber.subscription_path(project_id, SUBSCRIPTION_ID)

    # The subscriber pulls one message. Acknowledge it so it won't be redelivered.
    response = subscriber.pull(
        request={
            "subscription": subscription_path,
            "max_messages": 1,
        }
    )

    if not response.received_messages:
        return None

    received_message = response.received_messages[0]
    ack_id = received_message.ack_id
    message_data = json.loads(received_message.message.data.decode("utf-8"))
    message_id = received_message.message.message_id
    message_attributes = dict(received_message.message.attributes)

    subscriber.acknowledge(
        request={
            "subscription": subscription_path,
            "ack_ids": [ack_id],
        }
    )

    return ConsumeResponse(
        message=PubsubMessage(
            data=message_data, message_id=message_id, attributes=message_attributes
        ),
        ack_id=ack_id,
    )
