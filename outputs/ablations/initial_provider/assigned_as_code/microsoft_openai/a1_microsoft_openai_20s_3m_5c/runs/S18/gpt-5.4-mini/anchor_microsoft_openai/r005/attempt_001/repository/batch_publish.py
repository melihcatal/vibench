import json
import uuid
from azure.servicebus import ServiceBusClient, ServiceBusMessage
from messaging_client import load_messaging_config


def batch_publish(events, config=None):
    cfg = load_messaging_config(config)
    messages = []
    for event in events:
        event_id = str(event.get('id') or uuid.uuid4())
        messages.append(ServiceBusMessage(json.dumps(event), message_id=event_id, content_type='application/json'))
    with ServiceBusClient.from_connection_string(cfg['connection_string']) as client:
        with client.get_topic_sender(topic_name=cfg['topic']) as sender:
            sender.send_messages(messages)
    return {'message_ids': [message.message_id for message in messages]}
