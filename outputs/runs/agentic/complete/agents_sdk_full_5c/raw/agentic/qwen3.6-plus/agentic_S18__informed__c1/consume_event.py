"""
[SAME-SCENARIO] Consume one message from Google Cloud Pub/Sub managed subscription.
Provider: Google Cloud Pub/Sub
SDK: google-cloud-pubsub
Auth: GOOGLE_APPLICATION_CREDENTIALS
"""

import os
from typing import Optional
from messaging_models import PubSubEvent, ConsumeResult
from messaging_client import (
    get_pubsub_subscriber_client,
    get_subscription_path,
    consume_one_message,
    ack_message,
)


def consume_event(
    subscription_id: str = None,
    project_id: str = None,
    timeout_seconds: float = 10.0,
) -> ConsumeResult:
    """
    Consume exactly one message from a Google Cloud Pub/Sub subscription.

    Args:
        subscription_id: The Pub/Sub subscription identifier.
        project_id: The GCP project ID.
        timeout_seconds: How long to wait for a message.

    Returns:
        ConsumeResult with the deserialized event and ack status.
    """
    subscription_id = subscription_id or os.environ.get(
        "PUBSUB_SUBSCRIPTION_ID", "events-subscription"
    )
    subscriber = get_pubsub_subscriber_client()
    subscription_path = get_subscription_path(project_id, subscription_id)

    msg = consume_one_message(subscriber, subscription_path, timeout_seconds)
    if msg is None:
        return ConsumeResult(
            event=None,
            raw_message=None,
            message_id="",
            acknowledged=False,
        )

    event = PubSubEvent.from_raw_message(msg["data"], msg["attributes"])

    ack_message(subscriber, subscription_path, msg["ack_id"])

    return ConsumeResult(
        event=event,
        raw_message=msg["data"],
        message_id=msg["message_id"],
        attributes=msg["attributes"],
        acknowledged=True,
    )
