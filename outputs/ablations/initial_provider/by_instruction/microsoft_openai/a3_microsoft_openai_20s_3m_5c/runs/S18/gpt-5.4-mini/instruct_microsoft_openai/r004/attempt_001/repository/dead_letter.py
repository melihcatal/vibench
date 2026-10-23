from messaging_client import create_client, get_dead_letter_queue_name


def send_dead_letter(message):
    with create_client() as client:
        sender = client.get_queue_sender(queue_name=get_dead_letter_queue_name())
        with sender:
            sender.send_messages(str(message))
    return {"sent": True}
