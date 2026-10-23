import json
import os
from typing import Dict, Any, Optional
from google.cloud import pubsub_v1
from messaging_client import GOOGLE_CLOUD_PROJECT, EVENTS_SUB
from messaging_models import PubSubMessage

def consume_event() -> Optional[Dict[str, Any]]:
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(GOOGLE_CLOUD_PROJECT, EVENTS_SUB)
    request = pubsub_v1.types.PullRequest(
        subscription=subscription_path,
        max_messages=1,
    )
    response = subscriber.pull(request)
    if not response.received_messages:
        return None
    received_message = response.received_messages[0]
    pubsub_msg = PubSubMessage.from_received(received_message)
    message_data = pubsub_msg.payload()
    ack_request = pubsub_v1.types.AcknowledgeRequest(
        subscription=subscription_path,
        ack_ids=[received_message.ack_id],
    )
    subscriber.acknowledge(ack_request)
    return message_data
