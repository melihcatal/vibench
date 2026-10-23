from __future__ import annotations

from typing import Optional

from google.cloud.pubsub_v1.types import PullRequest

from messaging_client import subscriber_client, subscription_path
from messaging_models import ConsumedMessage, decode_message_data



def consume_one_message(
    subscription_id: Optional[str] = None,
    project_id: Optional[str] = None,
    auto_ack: bool = False,
) -> Optional[ConsumedMessage]:
    client = subscriber_client()
    sub_path = subscription_path(subscription_id=subscription_id, project_id=project_id)
    response = client.pull(
        request=PullRequest(subscription=sub_path, max_messages=1),
        timeout=10,
    )
    if not response.received_messages:
        return None

    received = response.received_messages[0]
    msg = received.message
    if auto_ack:
        client.acknowledge(request={"subscription": sub_path, "ack_ids": [received.ack_id]})

    return ConsumedMessage(
        ack_id=received.ack_id,
        message_id=msg.message_id,
        publish_time=msg.publish_time.isoformat() if msg.publish_time else None,
        data=decode_message_data(msg.data),
        attributes=dict(msg.attributes),
    )
