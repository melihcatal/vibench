import json

from messaging_client import create_client, load_config
from messaging_models import decode_json_bytes


def consume_event() -> dict:
    config = load_config()
    with create_client() as client:
        receiver = client.get_queue_receiver(
            queue_name=config.queue_name, max_wait_time=5
        )
        with receiver:
            messages = receiver.receive_messages(max_message_count=1, max_wait_time=5)
            if not messages:
                return {"message": None}
            message = messages[0]
            body = b"".join([bytes(part) for part in message.body])
            payload = decode_json_bytes(body)
            receiver.complete_message(message)
            return {"message_id": str(message.message_id), "payload": payload}


if __name__ == "__main__":
    print(json.dumps(consume_event()))
