from typing import Dict, Any, Optional

from messaging_client import subscription_path, subscriber
from messaging_models import parse_pubsub_message


def consume_event(subscription_name: str = "events-sub") -> Optional[Dict[str, Any]]:
    sub_p = subscription_path(subscription_name)
    response = subscriber.pull(
        subscription=sub_p,
        max_messages=1,
        return_immediately=True,
    )
    if not response.received_messages:
        return None
    message = response.received_messages[0]
    ack_id = message.ack_id
    msg_dict = parse_pubsub_message(message)
    subscriber.acknowledge(subscription=sub_p, ack_ids=[ack_id])
    return msg_dict
