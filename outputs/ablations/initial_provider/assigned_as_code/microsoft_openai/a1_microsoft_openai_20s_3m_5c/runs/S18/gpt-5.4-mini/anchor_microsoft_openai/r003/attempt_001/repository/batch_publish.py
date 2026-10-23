import json
import uuid
from azure.servicebus import ServiceBusMessage

from messaging_client import load_messaging_config, build_service_bus_client


def batch_publish(messages, config=None):
    config = load_messaging_config(config)
    published = []
    with build_service_bus_client(config) as client:
        with client.get_topic_sender(topic_name=config['topic']) as sender:
            batch = sender.create_message_batch()
            for item in messages:
                message_id = item.get('message_id') or str(uuid.uuid4())
                message = ServiceBusMessage(json.dumps(item['event']), message_id=message_id, application_properties=item.get('attributes') or {}, content_type='application/json')
                if not batch.try_add_message(message):
                    sender.send_messages(batch)
                    batch = sender.create_message_batch()
                    batch.try_add_message(message)
                published.append(message_id)
            if len(batch) > 0:
                sender.send_messages(batch)
    return {'message_ids': published}
