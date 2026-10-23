import os
from azure.servicebus import ServiceBusClient, ServiceBusMessage

os.environ['AZURE_SERVICE_BUS_CONNECTION_STRING'] = 'your_connection_string'
os.environ['AZURE_SERVICE_BUS_TOPIC'] = 'your_topic_name'

def publish_event(message):
    client = ServiceBusClient.from_connection_string(os.getenv('AZURE_SERVICE_BUS_CONNECTION_STRING'))
    with client:
        sender = client.get_topic_sender(os.getenv('AZURE_SERVICE_BUS_TOPIC'))
        with sender:
            sender.send_messages(ServiceBusMessage(message))

publish_event('{