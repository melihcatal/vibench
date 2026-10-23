import os
from azure.servicebus import ServiceBusClient, ServiceBusMessage

def batch_publish(messages):
    connection_str = os.getenv('AZURE_SERVICE_BUS_CONNECTION_STR')
    topic_name = os.getenv('AZURE_SERVICE_BUS_TOPIC')
    servicebus_client = ServiceBusClient.from_connection_string(conn_str=connection_str)
    with servicebus_client:
        sender = servicebus_client.get_topic_sender(topic_name)
        with sender:
            batch_message = sender.create_message_batch()
            for message in messages:
                if batch_message.add_message(ServiceBusMessage(message)):
                    continue
                else:
                    break
            sender.send_messages(batch_message)
            print(f'Batch published: {messages}')

if __name__ == '__main__':
    messages = ['{"key": "value"}', '{"key": "value2"}']
    batch_publish(messages)