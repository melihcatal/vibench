import os
from azure.servicebus import ServiceBusClient, ServiceBusMessage

os.environ['AZURE_SERVICE_BUS_CONNECTION_STRING'] = 'Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<keyName>;SharedAccessKey=<key>'

connection_str = os.getenv('AZURE_SERVICE_BUS_CONNECTION_STRING')
dead_letter_queue_name = 'events-dlq'

def dead_letter(message):
    with ServiceBusClient.from_connection_string(connection_str) as client:
        sender = client.get_queue_sender(dead_letter_queue_name)
        sender.send_messages(message)