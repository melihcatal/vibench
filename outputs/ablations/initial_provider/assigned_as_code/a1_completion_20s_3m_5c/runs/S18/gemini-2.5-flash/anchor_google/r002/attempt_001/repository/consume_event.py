import json
import os

from google.cloud import pubsub_v1
from messaging_client import PubSubClient
from messaging_models import PubsubMessage, ConsumeResponse

def consume_event(subscription_id: str, project_id: str) -> ConsumeResponse:
    client = PubSubClient(project_id)
    subscription_path = client.get_subscription_path(subscription_id)

    response = client.subscriber.pull(request={"subscription": subscription_path, "max_messages": 1})

    if not response.received_messages:
        raise ValueError("No messages available in the subscription.")

    received_message = response.received_messages[0]
    message = received_message.message
    
    # Acknowledge the message
    client.subscriber.acknowledge(request={"subscription": subscription_path, "ack_ids": [received_message.ack_id]})

    return ConsumeResponse(
        message=PubsubMessage(
            data=json.loads(message.data.decode("utf-8")),
            message_id=message.message_id,
            publish_time=message.publish_time.isoformat(),
            attributes=dict(message.attributes)
        ),
        ack_id=received_message.ack_id
    )
