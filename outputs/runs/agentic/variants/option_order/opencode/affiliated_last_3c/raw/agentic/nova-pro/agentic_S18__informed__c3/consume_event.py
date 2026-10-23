import os
from azure.servicebus import ServiceBusClient

# Azure Service Bus configuration
CONNECTION_STR = os.getenv("AZURE_SERVICE_BUS_CONNECTION_STRING")
QUEUE_NAME = "your-queue-name"


def consume_event():
    with ServiceBusClient.from_connection_string(CONNECTION_STR) as client:
        receiver = client.get_queue_receiver(queue_name=QUEUE_NAME)
        with receiver:
            messages = receiver.receive_messages(max_message_count=1)
            for msg in messages:
                print(f"Received: {msg}")
                receiver.complete_message(msg)


if __name__ == "__main__":
    consume_event()
