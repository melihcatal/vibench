import json
from azure.servicebus import ServiceBusMessage

from messaging_client import load_messaging_config, build_service_bus_client


def dead_letter_message(payload, config=None, reason='processing_failed'):
    config = load_messaging_config(config)
    with build_service_bus_client(config) as client:
        with client.get_queue_sender(queue_name=config['dead_letter_queue'] or config['queue']) as sender:
            sender.send_messages(ServiceBusMessage(json.dumps({'reason': reason, 'payload': payload}), content_type='application/json'))
    return {'sent': True, 'reason': reason}
