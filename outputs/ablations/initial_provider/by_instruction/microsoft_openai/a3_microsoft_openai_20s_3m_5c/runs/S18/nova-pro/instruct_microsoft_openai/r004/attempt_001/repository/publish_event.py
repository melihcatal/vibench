import os
from azure.servicebus import ServiceBusClient, ServiceBusMessage

def publish_event(event):
    connection_str = os.getenv('AZURE_SERVICE_BUS_CONNECTION_STR')
    topic_name = os.getenv('AZURE_SERVICE_BUS_TOPIC')
    servicebus_client = ServiceBusClient.from_connection_string(conn_str=connection_str)
    with servicebus_client:
        sender = servicebus_client.get_topic_sender(topic_name)
        with sender:
            message = ServiceBusMessage(event)
            sender.send_messages(message)
            print(f'Event published: {event}')

if __name__ == '__main__':
    event = '{"key": "value"}'
    publish_event(event)