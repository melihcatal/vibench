import os
from azure.servicebus import ServiceBusClient


def consume_event(queue_name):
    conn_str = os.getenv("AZURE_SERVICE_BUS_CONNECTION_STRING")
    with ServiceBusClient.from_connection_string(conn_str) as client:
        receiver = client.get_queue_receiver(queue_name)
        with receiver:
            messages = receiver.receive_messages(max_message_count=1)
            for message in messages:
                print(str(message))
                receiver.complete_message(message)


if __name__ == "__main__":
    consume_event("my_queue")
