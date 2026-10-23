import os
from azure.servicebus import ServiceBusClient

# Configuration
SERVICE_BUS_CONNECTION_STR = os.getenv("AZURE_SERVICE_BUS_CONNECTION_STRING")
SUBSCRIPTION_NAME = "your-subscription-name"
TOPIC_NAME = "your-topic-name"


# Consume one message from a managed subscription
def consume_event():
    with ServiceBusClient.from_connection_string(SERVICE_BUS_CONNECTION_STR) as client:
        receiver = client.get_subscription_receiver(TOPIC_NAME, SUBSCRIPTION_NAME)
        messages = receiver.receive_messages(max_message_count=1, max_wait_time=5)
        for message in messages:
            print(str(message))
            receiver.complete_message(message)


if __name__ == "__main__":
    consume_event()
