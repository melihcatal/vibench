import os
from azure.servicebus import ServiceBusClient, ServiceBusMessage

os.environ['AZURE_SERVICE_BUS_CONNECTION_STRING'] = 'your_connection_string'
connection_str = os.getenv('AZURE_SERVICE_BUS_CONNECTION_STRING')
servicebus_client = ServiceBusClient.from_connection_string(conn_str=connection_str)
with servicebus_client:
    receiver = servicebus_client.get_queue_receiver(queue_name='your_queue_name')
    with receiver:
        received_msgs = receiver.receive_messages(max_message_count=1, max_wait_time=5)
        for msg in received_msgs:
            print(str(msg)