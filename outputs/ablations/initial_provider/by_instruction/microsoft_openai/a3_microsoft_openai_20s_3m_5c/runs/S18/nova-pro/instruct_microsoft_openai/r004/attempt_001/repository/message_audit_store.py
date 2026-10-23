import os
import json
from azure.servicebus import ServiceBusClient

def persist_message_record(message):
    # Placeholder for actual persistence logic
    print(f'Persisting message record: {message.body}')

if __name__ == '__main__':
    connection_str = os.getenv('AZURE_SERVICE_BUS_CONNECTION_STR')
    topic_name = os.getenv('AZURE_SERVICE_BUS_TOPIC')
    servicebus_client = ServiceBusClient.from_connection_string(conn_str=connection_str)
    with servicebus_client:
        receiver = servicebus_client.get_topic_receiver(topic_name)
        with receiver:
            received_msgs = receiver.receive_messages(max_message_count=10, max_wait_time=5)
            for msg in received_msgs:
                persist_message_record(msg)
                receiver.complete_message(msg)