import os
from concurrent.futures import TimeoutError
from messaging_client import PubSubClient
from messaging_models import PubSubEvent
from google.cloud.pubsub_v1 import SubscriberClient

def consume_event(subscription_id: str, timeout: float = 5.0):
    client = PubSubClient()
    subscriber: SubscriberClient = client.get_subscriber_client()
    subscription_path = client.subscription_path(subscription_id)

    # The subscriber pulls a message. The client is aware of the subscription. Only exception handling is needed.
    try:
        response = subscriber.pull(request={
            "subscription": subscription_path,
            "max_messages": 1,
            "return_immediately": True
        })

        if not response.received_messages:
            return None

        received_message = response.received_messages[0]
        message = received_message.message

        event_data = message.data.decode("utf-8")
        pubsub_event = PubSubEvent.from_json(
            event_data,
            message_id=message.message_id,
            attributes=dict(message.attributes)
        )

        # Acknowledge the message so it is not redelivered.
        ack_ids = [received_message.ack_id]
        subscriber.acknowledge(request={"subscription": subscription_path, "ack_ids": ack_ids})

        return pubsub_event
    except Exception as e:
        print(f"Error consuming message: {e}")
        return None
