import json
from azure.servicebus import ServiceBusClient, ServiceBusMessage


def consume_event(config=None):
    config = config or {}
    with ServiceBusClient.from_connection_string(config['connection_string']) as client:
        with client.get_queue_receiver(queue_name=config['queue']) as receiver:
            received_msgs = receiver.receive_messages(max_message_count=1, max_wait_time=5)
            for msg in received_msgs:
                event = json.loads(msg.body)
                return {'event': event, 'message_id': msg.message_id}
    return None