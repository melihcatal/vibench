import json
import uuid
from azure.servicebus import ServiceBusClient, ServiceBusMessage


def consume_event(config=None):
    config = config or {}
    with ServiceBusClient.from_connection_string(config['connection_string']) as client:
        with client.get_subscription_receiver(topic_name=config['topic'], subscription_name=config['subscription']) as receiver:
            received_msgs = receiver.receive_messages(max_message_count=1, max_wait_time=5)
            if received_msgs:
                return json.loads(received_msgs[0].body)
    return None