from azure.servicebus import ServiceBusReceiveMode

from messaging_client import create_client, load_config, normalize_message_body
from messaging_models import ConsumeResult, json_to_payload


def consume_event():
    config = load_config()
    with create_client() as client:
        receiver = client.get_subscription_receiver(
            topic_name=config.topic_name,
            subscription_name=config.subscription_name,
            receive_mode=ServiceBusReceiveMode.PEEK_LOCK,
        )
        with receiver:
            messages = receiver.receive_messages(max_message_count=1, max_wait_time=5)
            if not messages:
                return None
            msg = messages[0]
            body = normalize_message_body(b"".join([bytes(part) for part in msg.body]))
            payload = json_to_payload(body)
            receiver.complete_message(msg)
            return ConsumeResult(
                message_id=payload.message_id,
                body=payload.content,
                delivery_count=msg.delivery_count,
            )
