import os
from azure.servicebus import ServiceBusClient, ServiceBusMessage

os.environ['AZURE_SERVICE_BUS_CONNECTION_STRING'] = 'Endpoint=sb://your-namespace.servicebus.windows.net/;SharedAccessKeyName=your-policy-name;SharedAccessKey=your-policy-key'

connection_str = os.getenv('AZURE_SERVICE_BUS_CONNECTION_STRING')
servicebus_client = ServiceBusClient.from_connection_string(conn_str=connection_str)
with servicebus_client:
    receiver = servicebus_client.get_queue_receiver(queue_name='your-queue-name')
    with receiver:
        received_msgs = receiver.receive_messages(max_message_count=10, max_wait_time=5)
        for msg in received_msgs:
            print(str(msg)