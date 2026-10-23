import os
from azure.servicebus import ServiceBusClient, ServiceBusMessage

os.environ['AZURE_SERVICE_BUS_CONNECTION_STRING'] = 'Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<keyName>;SharedAccessKey=<key>'

connection_str = os.getenv('AZURE_SERVICE_BUS_CONNECTION_STRING')
topic_name = 'events'

def batch_publish(events):
    with ServiceBusClient.from_connection_string(connection_str) as client:
        sender = client.get_topic_sender(topic_name)
        messages = [ServiceBusMessage(event) for event in events]
        sender.send_messages(messages)