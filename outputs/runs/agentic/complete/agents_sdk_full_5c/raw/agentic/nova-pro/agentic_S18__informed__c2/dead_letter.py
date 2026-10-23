import os
from azure.servicebus import ServiceBusClient, ServiceBusMessage

os.environ['AZURE_SERVICE_BUS_CONNECTION_STRING'] = 'your_connection_string'
connection_str = os.getenv('AZURE_SERVICE_BUS_CONNECTION_STRING')
servicebus_client = ServiceBusClient.from_connection_string(conn_str=connection_str)
with servicebus_client:
    sender = servicebus_client.get_queue_sender(queue_name='your_dead_letter_queue_name')
    message = ServiceBusMessage({"key": "value"})
    sender.send_messages(message)