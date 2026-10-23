import json
from typing import Optional

from messaging_client import create_service_bus_client, get_subscription_name, get_topic_name
from messaging_models import ConsumedMessage, normalize_message_body


def consume_event(max_wait_time: int = 5) -> Optional[ConsumedMessage]:
    client = create_service_bus_client()
    topic_name = get_topic_name()
    subscription_name = get_subscription_name()
    with client:
        receiver = client.get_subscription_receiver(
            topic_name=topic_name,
            subscription_name=subscription_name,
            max_wait_time=max_wait_time,
        )
        with receiver:
            messages = receiver.receive_messages(max_message_count=1, max_wait_time=max_wait_time)
            if not messages:
                return None
            msg = messages[0]
            body = "".join([part.decode("utf-8") if isinstance(part, bytes) else str(part) for part in msg.body])
            normalized = normalize_message_body(body)
            receiver.complete_message(msg)
            return ConsumedMessage(
                message_id=str(getattr(msg, "message_id", "")),
                body=normalized if normalized else {"raw": body},
                subject=getattr(msg, "subject", None),
                delivery_count=int(getattr(msg, "delivery_count", 0) or 0),
            )


if __name__ == "__main__":
    result = consume_event()
    print(json.dumps(result.body if result else {}, ensure_ascii=False))
