from google.cloud import pubsub_v1

from messaging_client import subscription_path, SUBSCRIPTION_ID
from messaging_models import PubSubMessage

def consume_event(max_messages: int = 1) -> list[PubSubMessage]:
    subscriber = pubsub_v1.SubscriberClient()
    subscription = subscription_path(SUBSCRIPTION_ID)
    response = subscriber.pull(
        request={
            'subscription': subscription,
            'max_messages': max_messages,
        },
    )
    messages = []
    ack_ids = []
    for received_message in response.received_messages:
        msg = PubSubMessage(
            message_id=received_message.message.message_id,
            data=received_message.message.data.decode('utf-8'),
            attributes=dict(received_message.message.attributes)
        )
        messages.append(msg)
        ack_ids.append(received_message.ack_id)
    if ack_ids:
        subscriber.acknowledge(
            request={
                'subscription': subscription,
                'ack_ids': ack_ids,
            },
        )
    return messages