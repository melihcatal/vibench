import json
from messaging_client import get_servicebus_client
from messaging_models import ConsumeResponse
import os

def consume_event(config=None):
    config = config or {}
    subscription_name = config.get('subscription_name') or os.environ.get("AZURE_SERVICE_BUS_SUBSCRIPTION_NAME")
    topic_name = config.get('topic_name') or os.environ.get("AZURE_SERVICE_BUS_TOPIC_NAME")

    if not subscription_name or not topic_name:
        raise ValueError("Subscription name and topic name must be provided in config or environment variables.")

    with get_servicebus_client(config) as servicebus_client:
        receiver = servicebus_client.get_subscription_receiver(topic_name=topic_name, subscription_name=subscription_name)
        with receiver:
            received_msgs = receiver.receive_messages(max_wait_time=5, max_message_count=1)
            for msg in received_msgs:
                payload = json.loads(str(msg))
                response = ConsumeResponse(
                    payload=payload,
                    message_id=msg.message_id,
                    sequence_number=msg.sequence_number,
                    lock_token=msg.lock_token
                )
                receiver.complete_message(msg)
                return response
    return None
