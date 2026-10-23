import json
from azure.servicebus import ServiceBusClient, ServiceBusMessage

from messaging_client import get_servicebus_client

def consume_event(config=None):
    config = config or {}
    client = get_servicebus_client(config['connection_string'])
    with client.get_subscription_receiver(topic_name=config['topic'], subscription_name=config['subscription'], max_wait_time=5) as receiver:
        for msg in receiver:
            event = json.loads(str(msg))
            receiver.complete_message(msg)
            return event