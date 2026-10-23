import os
import json
from google.cloud.pubsub_v1.subscriber import message
from messaging_client import PubSubClientHelper
from messaging_models import ConsumedMessage

def consume_event() -> ConsumedMessage:
    client_helper = PubSubClientHelper()
    subscriber = client_helper.get_subscriber_client()
    subscription_id = os.environ.get("GCP_PUBSUB_SUBSCRIPTION_ID")
    if not subscription_id:
        raise ValueError("GCP_PUBSUB_SUBSCRIPTION_ID environment variable not set.")

    subscription_path = client_helper.get_subscription_path(subscription_id)

    response = subscriber.pull(request={
        "subscription": subscription_path,
        "max_messages": 1,
        "return_immediately": True,
    })

    if not response.received_messages:
        raise RuntimeError("No messages received.")

    received_message = response.received_messages[0]
    msg: message.Message = received_message.message

    data_payload = json.loads(msg.data.decode("utf-8"))
    attributes = dict(msg.attributes)

    consumed_event = ConsumedMessage(
        event_id=attributes.get('event_id', 'unknown'),
        data=data_payload,
        attributes=attributes,
        message_id=msg.message_id,
        publish_time=msg.publish_time.isoformat(),
        ack_id=received_message.ack_id
    )

    # Acknowledge the message
    subscriber.acknowledge(
        request={
            "subscription": subscription_path,
            "ack_ids": [received_message.ack_id]
        }
    )

    return consumed_event
