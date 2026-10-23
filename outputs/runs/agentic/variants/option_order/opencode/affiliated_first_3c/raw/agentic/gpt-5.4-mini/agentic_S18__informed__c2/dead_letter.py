import os

from azure.servicebus import ServiceBusMessage

from messaging_client import build_client, load_config


def send_to_dead_letter(payload: dict) -> str | None:
    config = load_config()
    with build_client() as client:
        sender = client.get_queue_sender(
            queue_name=config.dead_letter_queue_name
            or os.environ["AZURE_SERVICE_BUS_DEAD_LETTER_QUEUE_NAME"]
        )
        with sender:
            message = ServiceBusMessage(
                str(payload), application_properties={"dead_letter": True}
            )
            sender.send_messages(message)
            return getattr(message, "message_id", None)
