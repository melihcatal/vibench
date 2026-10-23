import json
import uuid

from azure.servicebus import ServiceBusMessage

from messaging_client import get_client
from messaging_models import normalize_payload, response_payload


def batch_publish(items, config=None):
    client, cfg = get_client(config)
    messages = []
    message_ids = []
    for item in items:
        payload = normalize_payload(item)
        message_id = str(payload.get('id') or uuid.uuid4())
        message_ids.append(message_id)
        messages.append(ServiceBusMessage(json.dumps(payload), message_id=message_id, content_type='application/json'))
    with client:
        with client.get_topic_sender(topic_name=cfg['topic']) as sender:
            sender.send_messages(messages)
    return response_payload('published', message_ids=message_ids)
