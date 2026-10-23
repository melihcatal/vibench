from google.cloud import pubsub_v1
import messaging_client
from messaging_models import pubsub_message_to_dict
from typing import Dict, Any, Optional


def consume_event() -> Optional[Dict[str, Any]]:
    """
    Consumes one message from the configured Pub/Sub subscription and acknowledges it.
    """
    try:
        client = pubsub_v1.SubscriberClient()
        subscription_path = client.subscription_path(
            messaging_client.PUBSUB_PROJECT_ID, messaging_client.PUBSUB_SUBSCRIPTION
        )
        response = client.pull(
            request={"subscription": subscription_path, "max_messages": 1}
        )
        if not response.received_messages:
            return None
        msg = response.received_messages[0]
        msg_dict = pubsub_message_to_dict(msg)
        client.acknowledge(
            request={"subscription": subscription_path, "ack_ids": [msg.ack_id]}
        )
        return msg_dict
    except Exception:
        return None
