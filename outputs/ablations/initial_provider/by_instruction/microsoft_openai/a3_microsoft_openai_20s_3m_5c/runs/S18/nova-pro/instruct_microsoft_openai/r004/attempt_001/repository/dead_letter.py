import os
from azure.servicebus import ServiceBusClient, ServiceBusMessage

def dead_letter(message):
    connection_str = os.getenv('AZURE_SERVICE_BUS_CONNECTION_STR')
    dead_letter_queue_name = os.getenv('AZURE_SERVICE_BUS_DEAD_LETTER_QUEUE')
    servicebus_client = ServiceBusClient.from_connection_string(conn_str=connection_str)
    with servicebus_client:
        sender = servicebus_client.get_queue_sender(dead_letter_queue_name)
        with sender:
            dead_letter_message = ServiceBusMessage(message)
            sender.send_messages(dead_letter_message)
            print(f'Message sent to dead letter queue: {message}')

if __name__ == '__main__':
    message = '{"key": "value"}'
    dead_letter(message)