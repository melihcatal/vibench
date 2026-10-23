from azure.servicebus import ServiceBusClient, ServiceBusMessage

from messaging_client import get_servicebus_client

def dead_letter(message, config=None):
    config = config or {}
    client = get_servicebus_client(config['connection_string'])
    with client.get_queue_sender(queue_name=config['dead_letter_queue']) as sender:
        sender.send_messages(ServiceBusMessage(message))