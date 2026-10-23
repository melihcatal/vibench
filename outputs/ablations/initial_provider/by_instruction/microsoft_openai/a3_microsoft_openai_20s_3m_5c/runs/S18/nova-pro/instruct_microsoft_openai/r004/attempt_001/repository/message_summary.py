import os
import json
from azure.servicebus import ServiceBusClient

def summarize_message_processing(messages):
    summarized_results = {}
    for message in messages:
        message_body = json.loads(message.body)
        for key, value in message_body.items():
            if key not in summarized_results:
                summarized_results[key] = []
            summarized_results[key].append(value)
    return summarized_results

if __name__ == '__main__':
    connection_str = os.getenv('AZURE_SERVICE_BUS_CONNECTION_STR')
    topic_name = os.getenv('AZURE_SERVICE_BUS_TOPIC')
    servicebus_client = ServiceBusClient.from_connection_string(conn_str=connection_str)
    with servicebus_client:
        receiver = servicebus_client.get_topic_receiver(topic_name)
        with receiver:
            received_msgs = receiver.receive_messages(max_message_count=10, max_wait_time=5)
            summary = summarize_message_processing(received_msgs)
            print(f'Message processing summary: {summary}')
            for msg in received_msgs:
                receiver.complete_message(msg)