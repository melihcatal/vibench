import os
from azure.servicebus import ServiceBusClient, ServiceBusMessage


def dead_letter(queue_name, message):
    conn_str = os.getenv("AZURE_SERVICE_BUS_CONNECTION_STRING")
    with ServiceBusClient.from_connection_string(conn_str) as client:
        sender = client.get_queue_sender(queue_name)
        with sender:
            sender.send_messages(ServiceBusMessage(message))


if __name__ == "__main__":
    dead_letter("dead_letter_queue", '{"key": "value"}')
