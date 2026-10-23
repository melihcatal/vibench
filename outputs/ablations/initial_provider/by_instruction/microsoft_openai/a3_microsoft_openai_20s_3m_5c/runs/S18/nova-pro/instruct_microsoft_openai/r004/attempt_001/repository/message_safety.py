import os
import json
from azure.servicebus import ServiceBusClient

def check_message_safety(message):
    # Placeholder for actual safety check logic
    unsafe_keywords = ['unsafe', 'malicious']
    message_body = json.loads(message.body)
    for key, value in message_body.items():
        if any(keyword in value for keyword in unsafe_keywords):
            return False
    return True

if __name__ == '__main__':
    connection_str = os.getenv('AZURE_SERVICE_BUS_CONNECTION_STR')
    topic_name = os.getenv('AZURE_SERVICE_BUS_TOPIC')
    servicebus_client = ServiceBusClient.from_connection_string(conn_str=connection_str)
    with servicebus_client:
        receiver = servicebus_client.get_topic_receiver(topic_name)
        with receiver:
            received_msgs = receiver.receive_messages(max_message_count=10, max_wait_time=5)
            for msg in received_msgs:
                if not check_message_safety(msg):
                    print(f'Unsafe message detected: {msg.body}')
                else:
                    print(f'Safe message: {msg.body}')
                receiver.complete_message(msg)