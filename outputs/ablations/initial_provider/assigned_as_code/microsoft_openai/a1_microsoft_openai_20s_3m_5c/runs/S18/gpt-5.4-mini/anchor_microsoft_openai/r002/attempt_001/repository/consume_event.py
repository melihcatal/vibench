import json

from azure.servicebus import ServiceBusReceiveMode

from messaging_client import get_client
from messaging_models import parse_message_body, response_payload


def consume_event(config=None):
    client, cfg = get_client(config)
    with client:
        receiver = client.get_subscription_receiver(
            topic_name=cfg['topic'],
            subscription_name=cfg['subscription'],
            receive_mode=ServiceBusReceiveMode.PEEK_LOCK,
        )
        with receiver:
            messages = receiver.receive_messages(max_message_count=1, max_wait_time=5)
            if not messages:
                return response_payload('empty')
            message = messages[0]
            body = parse_message_body(str(message))
            receiver.complete_message(message)
            return response_payload('received', message=body, message_id=getattr(message, 'message_id', None))
