from google.cloud import pubsub_v1
from messaging_client import SUBSCRIPTION_PATH
from messaging_models import PubSubMessage


def consume_event() -> PubSubMessage | None:
    subscriber = pubsub_v1.SubscriberClient()
    response = subscriber.pull(subscription=SUBSCRIPTION_PATH, max_messages=1)
    if not response.received_messages:
        return None
    received_msg = response.received_messages[0]
    message = received_msg.message
    psm = PubSubMessage(
        message_id=message.message_id,
        data=message.data,
        attributes=dict(message.attributes),
        publish_time=message.publish_time.ToDatetime().isoformat(),
        ack_id=received_msg.ack_id,
    )
    subscriber.acknowledge(
        subscription=SUBSCRIPTION_PATH, ack_ids=[received_msg.ack_id]
    )
    return psm
