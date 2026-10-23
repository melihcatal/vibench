import json
from azure.servicebus import ServiceBusClient, ServiceBusMessage


def batch_publish(payloads, config=None):
    config = config or {}
    message_ids = []
    with ServiceBusClient.from_connection_string(config['connection_string']) as client:
        with client.get_topic_sender(topic_name=config['topic']) as sender:
            for payload in payloads:
                message_id = str(uuid.uuid4())
                sender.send_messages(ServiceBusMessage(json.dumps(payload['event']),
                    message_id=message_id, content_type='application/json'))
                message_ids.append(message_id)
    return {'message_ids': message_ids}