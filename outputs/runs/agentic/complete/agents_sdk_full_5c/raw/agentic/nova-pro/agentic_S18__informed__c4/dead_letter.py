import os
from azure.servicebus import ServiceBusClient, ServiceBusMessage

os.environ['AZURE_SERVICE_BUS_CONNECTION_STRING'] = 'Endpoint=sb://your-namespace.servicebus.windows.net/;SharedAccessKeyName=your-policy-name;SharedAccessKey=your-policy-key'

connection_str = os.getenv('AZURE_SERVICE_BUS_CONNECTION_STRING')
servicebus_client = ServiceBusClient.from_connection_string(conn_str=connection_str)
with servicebus_client:
    sender = servicebus_client.get_queue_sender(queue_name='your-dead-letter-queue-name')
    with sender:
        message = ServiceBusMessage({"key": "value"})
        sender.send_messages(message)