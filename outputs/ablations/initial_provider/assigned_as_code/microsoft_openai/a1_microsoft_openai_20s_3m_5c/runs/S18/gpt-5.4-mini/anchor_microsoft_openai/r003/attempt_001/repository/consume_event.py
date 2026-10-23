import json
from azure.servicebus import ServiceBusReceiveMode

from messaging_client import load_messaging_config, build_service_bus_client
from messaging_models import normalize_message_body, make_result


def consume_event(config=None):
    config = load_messaging_config(config)
    with build_service_bus_client(config) as client:
        with client.get_subscription_receiver(
            topic_name=config['topic'],
            subscription_name=config['subscription'],
            receive_mode=ServiceBusReceiveMode.RECEIVE_AND_DELETE,
            max_wait_time=5,
        ) as receiver:
            messages = receiver.receive_messages(max_message_count=1, max_wait_time=5)
            if not messages:
                return make_result('empty')
            message = messages[0]
            body = normalize_message_body(message)
            return make_result('received', message_id=getattr(message, 'message_id', None), payload=body)
