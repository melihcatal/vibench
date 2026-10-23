import json
from azure.servicebus import ServiceBusMessage
from messaging_client import open_client, queue_name


def dead_letter(message, config=None):
    config = config or {}
    with open_client(config) as client:
        with client.get_queue_sender(queue_name(config)) as sender:
            sender.send_messages(ServiceBusMessage(json.dumps({'dead_letter': message}), content_type='application/json'))
    return {'status': 'sent'}
