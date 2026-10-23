import json

from messaging_client import create_client, load_config


def consume_one_message():
    config = load_config()
    with create_client() as client:
        receiver = client.get_queue_receiver(queue_name=config.queue_name, max_wait_time=5)
        with receiver:
            messages = next(receiver.receive_messages(max_message_count=1), None)
            if messages is None:
                return None
            body = b"".join([chunk for chunk in messages.body])
            receiver.complete_message(messages)
            return json.loads(body.decode("utf-8"))
