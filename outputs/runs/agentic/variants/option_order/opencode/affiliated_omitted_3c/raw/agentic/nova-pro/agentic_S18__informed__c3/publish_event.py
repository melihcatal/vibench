import os
from azure.servicebus import ServiceBusClient, ServiceBusMessage


def publish_event(topic_name, event):
    conn_str = os.getenv("AZURE_SERVICE_BUS_CONNECTION_STRING")
    with ServiceBusClient.from_connection_string(conn_str) as client:
        sender = client.get_topic_sender(topic_name)
        with sender:
            sender.send_messages(ServiceBusMessage(event))


if __name__ == "__main__":
    publish_event("my_topic", '{"key": "value"}')
