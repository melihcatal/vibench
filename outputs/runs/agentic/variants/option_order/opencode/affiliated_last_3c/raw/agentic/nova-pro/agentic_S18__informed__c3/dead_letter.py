import os
from azure.servicebus import ServiceBusClient

# Azure Service Bus configuration
CONNECTION_STR = os.getenv("AZURE_SERVICE_BUS_CONNECTION_STRING")
QUEUE_NAME = "your-queue-name"
DEAD_LETTER_QUEUE = "your-dead-letter-queue-name"


def dead_letter(message):
    with ServiceBusClient.from_connection_string(CONNECTION_STR) as client:
        sender = client.get_queue_sender(queue_name=DEAD_LETTER_QUEUE)
        with sender:
            sender.send_messages(ServiceBusMessage(message))


if __name__ == "__main__":
    message = {"key": "value"}
    dead_letter(message)
