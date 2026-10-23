import os
from azure.servicebus import ServiceBusClient, ServiceBusMessage

os.environ['AZURE_SERVICE_BUS_CONNECTION_STRING'] = 'your_connection_string'
os.environ['AZURE_SERVICE_BUS_SUBSCRIPTION'] = 'your_subscription_name'

def consume_event():
    client = ServiceBusClient.from_connection_string(os.getenv('AZURE_SERVICE_BUS_CONNECTION_STRING'))
    with client:
        receiver = client.get_subscription_receiver(os.getenv('AZURE_SERVICE_BUS_SUBSCRIPTION'))
        with receiver:
            messages = receiver.receive_messages(max_message_count=1)
            for message in messages:
                print(message)
                receiver.complete_message(message)

consume_event()