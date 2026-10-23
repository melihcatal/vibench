import os
from azure.servicebus import ServiceBusClient, ServiceBusMessage

def batch_publish(topic_name, messages):
    connection_str = os.getenv('SERVICE_BUS_CONNECTION_STR')
    with ServiceBusClient.from_connection_string(conn_str=connection_str) as client:
        sender = client.get_topic_sender(topic_name)
        servicebus_messages = [ServiceBusMessage(msg) for msg in messages]
        sender.send_messages(servicebus_messages)