import json
from azure.servicebus import ServiceBusClient, ServiceBusMessage


def dead_letter(payload, config=None):
    config = config or {}
    message_id = payload.get('message_id')
    with ServiceBusClient.from_connection_string(config['connection_string']) as client:
        with client.get_queue_sender(queue_name=config['dead_letter_queue']) as sender:
            sender.send_messages(ServiceBusMessage(json.dumps(payload['event']), message_id=message_id, content_type='application/json'))
    return {'message_id': message_id}