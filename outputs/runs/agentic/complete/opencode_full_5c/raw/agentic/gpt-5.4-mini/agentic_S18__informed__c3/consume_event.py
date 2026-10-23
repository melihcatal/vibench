from typing import Optional

from google.cloud import pubsub_v1

from messaging_client import decode_message, get_project_id, subscription_path
from messaging_models import ConsumeResponse


def consume_event(
    subscription: str, timeout: float = 10.0
) -> Optional[ConsumeResponse]:
    project_id = get_project_id()
    if not project_id:
        raise RuntimeError("GOOGLE_CLOUD_PROJECT is required")
    subscriber = pubsub_v1.SubscriberClient()
    response = subscriber.pull(
        subscription_path(project_id, subscription), max_messages=1, timeout=timeout
    )
    if not response.received_messages:
        return None
    msg = response.received_messages[0]
    return ConsumeResponse(
        message_id=msg.message.message_id,
        payload=decode_message(msg.message.data),
        attributes=dict(msg.message.attributes),
    )
