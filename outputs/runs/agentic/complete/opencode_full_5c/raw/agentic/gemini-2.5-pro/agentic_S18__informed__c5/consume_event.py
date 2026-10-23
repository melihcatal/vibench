import os
from google.cloud import pubsub_v1

from messaging_client import get_subscriber_client, get_project_id, SUBSCRIPTION_ID


def consume_event():
    """Consumes a single message from a Google Cloud Pub/Sub subscription."""
    project_id = get_project_id()
    if not project_id:
        raise ValueError("GCP project ID not set.")

    subscriber = get_subscriber_client()
    subscription_path = subscriber.subscription_path(project_id, SUBSCRIPTION_ID)

    response = subscriber.pull(
        request={"subscription": subscription_path, "max_messages": 1}
    )

    if not response.received_messages:
        return None

    received_message = response.received_messages[0]

    ack_id = received_message.ack_id
    subscriber.acknowledge(
        request={"subscription": subscription_path, "ack_ids": [ack_id]}
    )

    return received_message.message
