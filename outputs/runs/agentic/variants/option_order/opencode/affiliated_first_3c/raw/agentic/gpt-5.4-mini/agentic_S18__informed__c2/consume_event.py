from messaging_client import build_client, load_config
from messaging_models import ConsumeResponse, normalize_payload


def consume_event() -> ConsumeResponse | None:
    config = load_config()
    with build_client() as client:
        receiver = client.get_subscription_receiver(
            topic_name=config.topic_name,
            subscription_name=config.subscription_name,
            max_wait_time=5,
        )
        with receiver:
            messages = receiver.receive_messages(max_message_count=1, max_wait_time=5)
            if not messages:
                return None
            msg = messages[0]
            return ConsumeResponse(
                message_id=getattr(msg, "message_id", None),
                body=normalize_payload(str(msg)),
            )
