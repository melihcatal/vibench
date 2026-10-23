import os
from azure.servicebus import ServiceBusClient, ServiceBusMessage

os.environ['AZURE_SERVICE_BUS_CONNECTION_STRING'] = 'Endpoint=sb://<namespace>.servicebus.windows.net/;SharedAccessKeyName=<keyName>;SharedAccessKey=<key>'

connection_str = os.getenv('AZURE_SERVICE_BUS_CONNECTION_STRING')
subscription_name = 'events-sub'

def consume_event():
    with ServiceBusClient.from_connection_string(connection_str) as client:
        receiver = client.get_subscription_receiver('events', subscription_name)
        messages = receiver.receive_messages(max_message_count=1)
        for msg in messages:
            print(str(msg))
            msg.complete()