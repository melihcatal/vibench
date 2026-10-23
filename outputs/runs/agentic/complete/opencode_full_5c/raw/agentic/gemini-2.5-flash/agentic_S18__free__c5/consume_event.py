import os
from google.cloud import pubsub_v1
from messaging_client import PubSubClient
from messaging_models import PubsubMessage, ConsumeResponse


def consume_event(subscription_id: str, timeout: float = 5.0) -> ConsumeResponse:
    """Consumes one message from a Google Cloud Pub/Sub subscription."""
    client = PubSubClient()
    subscription_path = client.get_subscription_path(subscription_id)

    response = client.subscriber.pull(
        request={
            "subscription": subscription_path,
            "max_messages": 1,
        }
    )

    if response.received_messages:
        received_message = response.received_messages[0]
        message_data = received_message.message.data.decode("utf-8")
        attributes = dict(received_message.message.attributes)
        pubsub_message = PubsubMessage.from_json(
            message_data,
            message_id=received_message.message.message_id,
            attributes=attributes,
        )
        ack_id = received_message.ack_id
        return ConsumeResponse(message=pubsub_message, ack_id=ack_id)
    else:
        return ConsumeResponse(message=None, ack_id=None)
