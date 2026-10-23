from messaging_client import get_subscriber_client, get_project_id
from messaging_models import PubSubMessage
from google.cloud.pubsub_v1.subscriber.message import Message
import json


def consume_event(subscription_id: str, timeout: int = 5) -> PubSubMessage or None:
    """Consumes one message from a Google Cloud Pub/Sub subscription.

    Args:
        subscription_id: The ID of the Pub/Sub subscription.
        timeout: The maximum number of seconds to wait for a message.

    Returns:
        A PubSubMessage object if a message is received, otherwise None.
    """
    subscriber = get_subscriber_client()
    project_id = get_project_id()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    response = subscriber.pull(
        request={
            "subscription": subscription_path,
            "max_messages": 1,
        }
    )

    if response.received_messages:
        received_message = response.received_messages[0]
        message_data = received_message.message.data.decode("utf-8")
        message_attributes = dict(received_message.message.attributes)
        message_id = received_message.message.message_id

        # Acknowledge the message to remove it from the subscription
        ack_ids = [received_message.ack_id]
        subscriber.acknowledge(
            request={"subscription": subscription_path, "ack_ids": ack_ids}
        )

        return PubSubMessage(
            json.loads(message_data),
            message_id=message_id,
            attributes=message_attributes,
        )
    return None
