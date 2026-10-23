import os
import json
from azure.servicebus import ServiceBusClient

def translate_payload(message, target_language='es'):
    # Placeholder for actual translation logic
    translated_message = message.replace('en', target_language)
    return translated_message

if __name__ == '__main__':
    connection_str = os.getenv('AZURE_SERVICE_BUS_CONNECTION_STR')
    topic_name = os.getenv('AZURE_SERVICE_BUS_TOPIC')
    servicebus_client = ServiceBusClient.from_connection_string(conn_str=connection_str)
    with servicebus_client:
        receiver = servicebus_client.get_topic_receiver(topic_name)
        with receiver:
            received_msgs = receiver.receive_messages(max_message_count=10, max_wait_time=5)
            for msg in received_msgs:
                translated_msg = translate_payload(msg.body)
                print(f'Translated message: {translated_msg}')
                receiver.complete_message(msg)