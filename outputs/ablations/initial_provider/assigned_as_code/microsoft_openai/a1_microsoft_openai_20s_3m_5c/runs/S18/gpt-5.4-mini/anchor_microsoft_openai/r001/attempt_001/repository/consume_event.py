import json
from azure.servicebus import ServiceBusReceiveMode
from messaging_client import open_client, queue_name


def consume_event(config=None):
    config = config or {}
    with open_client(config) as client:
        with client.get_queue_receiver(queue_name(config), receive_mode=ServiceBusReceiveMode.RECEIVE_AND_DELETE) as receiver:
            messages = list(receiver.receive_messages(max_message_count=1, max_wait_time=5))
            if not messages:
                return {'message': None}
            message = messages[0]
            body = b''.join([bytes(part) for part in message.body]).decode('utf-8')
            return {'message_id': getattr(message, 'message_id', None), 'payload': json.loads(body)}
