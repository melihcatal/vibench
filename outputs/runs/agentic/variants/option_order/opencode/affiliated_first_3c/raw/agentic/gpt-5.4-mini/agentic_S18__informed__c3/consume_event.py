import json

from messaging_client import create_client, get_queue_name
from messaging_models import ConsumeResult


def consume_event():
    client = create_client()
    with client:
        receiver = client.get_queue_receiver(
            queue_name=get_queue_name(), max_wait_time=5
        )
        with receiver:
            messages = list(
                receiver.receive_messages(max_message_count=1, max_wait_time=5)
            )
            if not messages:
                return None
            message = messages[0]
            body = "".join(
                part.decode("utf-8") if isinstance(part, bytes) else str(part)
                for part in message.body
            )
            receiver.complete_message(message)
            return ConsumeResult(
                message_id=getattr(message, "message_id", ""),
                body=body,
                attributes=dict(getattr(message, "application_properties", {})),
                provider="azure-servicebus",
            )


def main():
    result = consume_event()
    print(json.dumps(None if result is None else result.__dict__, ensure_ascii=False))


if __name__ == "__main__":
    main()
