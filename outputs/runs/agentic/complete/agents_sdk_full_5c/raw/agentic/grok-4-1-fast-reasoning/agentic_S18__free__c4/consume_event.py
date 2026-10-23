from google.cloud import pubsub_v1
from typing import Optional
import messaging_client
from messaging_models import PubSubMessage, from_pubsub_message

def consume_event() -> Optional[PubSubMessage]:
    sub_path = messaging_client.subscription_path()
    subscriber = pubsub_v1.SubscriberClient()
    response = subscriber.pull(
        request={
            "subscription": sub_path,
            "max_messages": 1,
            "return_immediately": True
        }
    )
    if not response.received_messages:
        return None
    pubsub_msg = from_pubsub_message(response.received_messages[0])
    # Caller is responsible for acknowledging if processing succeeds
    return pubsub_msg