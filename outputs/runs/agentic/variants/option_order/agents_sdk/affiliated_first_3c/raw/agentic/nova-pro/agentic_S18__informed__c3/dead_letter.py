import os
from azure.servicebus import ServiceBusClient, ServiceBusMessage

os.environ['AZURE_SERVICE_BUS_CONNECTION_STRING'] = 'your_connection_string'
os.environ['AZURE_SERVICE_BUS_DEAD_LETTER_QUEUE'] = 'your_dead_letter_queue_name'

def dead_letter(message):
    client = ServiceBusClient.from_connection_string(os.getenv('AZURE_SERVICE_BUS_CONNECTION_STRING'))
    with client:
        sender = client.get_queue_sender(os.getenv('AZURE_SERVICE_BUS_DEAD_LETTER_QUEUE'))
        with sender:
            sender.send_messages(ServiceBusMessage(message))

dead_letter('Failed message')