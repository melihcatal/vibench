from azure.servicebus import ServiceBusMessage

from messaging_client import get_client
from messaging_models import normalize_payload, response_payload


def dead_letter(payload, config=None):
    client, cfg = get_client(config)
    body = normalize_payload(payload)
    with client:
        with client.get_queue_sender(queue_name=cfg['dead_letter_queue']) as sender:
            sender.send_messages(ServiceBusMessage(str(body), content_type='application/json'))
    return response_payload('sent', queue=cfg['dead_letter_queue'])
