import os
from azure.servicebus import ServiceBusClient, ServiceBusMessage

def publish_event(topic_name, message):
    connection_str = os.getenv('SERVICE_BUS_CONNECTION_STR')
    with ServiceBusClient.from_connection_string(conn_str=connection_str) as client:
        sender = client.get_topic_sender(topic_name)
        servicebus_message = ServiceBusMessage(message)
        sender.send_messages(servicebus_message)