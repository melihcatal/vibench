from azure.servicebus import ServiceBusClient
from messaging_client import get_servicebus_client
import os
import json

def consume_event(subscription_name, queue_name=None, topic_name=None):
    connection_string = os.environ.get("AZURE_SERVICE_BUS_CONNECTION_STRING")
    client = get_servicebus_client(connection_string)
    if queue_name:
        receiver = client.get_queue_receiver(queue_name=queue_name)
    elif topic_name and subscription_name:
        receiver = client.get_subscription_receiver(topic_name=topic_name, subscription_name=subscription_name)
    else:
        raise ValueError("Either queue_name or both topic_name and subscription_name must be provided.")

    with receiver:
        received_msgs = receiver.receive_messages(max_messages=1, max_wait_time=5)
        if received_msgs:
            for msg in received_msgs:
                message_body = str(msg)
                # Complete the message to remove it from the subscription
                receiver.complete_message(msg)
                return {
                    "message_id": msg.message_id,
                    "content_type": msg.content_type,
                    "body": json.loads(message_body) if msg.content_type == "application/json" else message_body,
                    "attributes": dict(msg.application_properties) if msg.application_properties else {}
                }
        else:
            return None
