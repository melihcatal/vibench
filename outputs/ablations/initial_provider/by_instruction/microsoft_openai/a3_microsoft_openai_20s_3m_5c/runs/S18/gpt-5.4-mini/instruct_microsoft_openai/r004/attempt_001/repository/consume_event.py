from messaging_client import create_client, get_queue_name
from messaging_models import parse_message


def consume_event():
    with create_client() as client:
        receiver = client.get_queue_receiver(queue_name=get_queue_name(), max_wait_time=5)
        with receiver:
            messages = list(receiver.receive_messages(max_message_count=1, max_wait_time=5))
            if not messages:
                return None
            message = messages[0]
            parsed = parse_message(message)
            receiver.complete_message(message)
            return parsed
