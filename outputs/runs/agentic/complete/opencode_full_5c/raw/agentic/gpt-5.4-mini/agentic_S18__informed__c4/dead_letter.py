from azure.servicebus import ServiceBusMessage

from messaging_client import create_client, load_config


def dead_letter_message(message_id, reason):
    config = load_config()
    with create_client() as client:
        sender = client.get_queue_sender(queue_name=config.dead_letter_queue)
        with sender:
            sender.send_messages(
                ServiceBusMessage({"message_id": message_id, "reason": reason})
            )
    return {"dead_lettered": True, "message_id": message_id}
