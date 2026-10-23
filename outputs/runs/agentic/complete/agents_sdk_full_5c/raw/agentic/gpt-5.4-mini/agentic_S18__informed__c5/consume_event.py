from __future__ import annotations

from typing import Optional

from google.cloud import pubsub_v1

from messaging_client import DEFAULT_SUBSCRIPTION_ID, subscription_path
from messaging_models import ConsumeResponse, envelope_from_json


def consume_one_message(
    subscription_id: str = DEFAULT_SUBSCRIPTION_ID,
    project_id: Optional[str] = None,
    timeout: float = 10.0,
) -> Optional[ConsumeResponse]:
    subscriber = pubsub_v1.SubscriberClient()
    response = subscriber.pull(
        request={
            "subscription": subscription_path(subscription_id, project_id),
            "max_messages": 1,
        },
        timeout=timeout,
    )
    if not response.received_messages:
        return None

    received = response.received_messages[0]
    payload = envelope_from_json(received.message.data.decode("utf-8"))
    subscriber.acknowledge(
        request={
            "subscription": subscription_path(subscription_id, project_id),
            "ack_ids": [received.ack_id],
        }
    )
    return ConsumeResponse(
        message_id=payload.message_id,
        payload=payload.payload,
        attributes=payload.attributes,
        raw={"ack_id": received.ack_id},
    )
