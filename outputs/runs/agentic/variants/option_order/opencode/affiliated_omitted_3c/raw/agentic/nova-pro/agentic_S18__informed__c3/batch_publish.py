import os
from azure.servicebus import ServiceBusClient, ServiceBusMessage


def batch_publish(topic_name, messages):
    conn_str = os.getenv("AZURE_SERVICE_BUS_CONNECTION_STRING")
    with ServiceBusClient.from_connection_string(conn_str) as client:
        sender = client.get_topic_sender(topic_name)
        with sender:
            sb_messages = [ServiceBusMessage(msg) for msg in messages]
            sender.send_messages(sb_messages)


if __name__ == "__main__":
    batch_publish("my_topic", ['{"key": "value1"}', '{"key": "value2"}'])
