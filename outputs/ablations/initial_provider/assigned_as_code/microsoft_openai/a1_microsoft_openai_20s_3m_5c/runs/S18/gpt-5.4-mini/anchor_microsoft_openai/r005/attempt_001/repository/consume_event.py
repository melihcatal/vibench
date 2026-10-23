from azure.servicebus import ServiceBusClient
from messaging_client import load_messaging_config


def consume_event(config=None):
    cfg = load_messaging_config(config)
    with ServiceBusClient.from_connection_string(cfg['connection_string']) as client:
        with client.get_subscription_receiver(topic_name=cfg['topic'], subscription_name=cfg['subscription']) as receiver:
            messages = list(receiver.receive_messages(max_message_count=1, max_wait_time=5))
            if not messages:
                return {'message': None}
            message = messages[0]
            receiver.complete_message(message)
            return {'message_id': str(message.message_id), 'body': str(message)}
