import os
from azure.servicebus import ServiceBusClient

# Configuration
SERVICE_BUS_CONNECTION_STR = os.getenv("AZURE_SERVICE_BUS_CONNECTION_STRING")
DEAD_LETTER_QUEUE_NAME = "your-dead-letter-queue-name"


# Send failed messages to a dead-letter destination
def dead_letter(message):
    with ServiceBusClient.from_connection_string(SERVICE_BUS_CONNECTION_STR) as client:
        sender = client.get_queue_sender(DEAD_LETTER_QUEUE_NAME)
        sender.send_messages(message)


if __name__ == "__main__":
    message = "Failed message"
    dead_letter(message)
