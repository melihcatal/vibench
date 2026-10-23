import os
from azure.servicebus import ServiceBusClient

def consume_event():
    connection_str = os.getenv('AZURE_SERVICE_BUS_CONNECTION_STR')
    subscription_name = os.getenv('AZURE_SERVICE_BUS_SUBSCRIPTION')
    servicebus_client = ServiceBusClient.from_connection_string(conn_str=connection_str)
    with servicebus_client:
        receiver = servicebus_client.get_subscription_receiver(subscription_name)
        with receiver:
            received_msgs = receiver.receive_messages(max_message_count=1, max_wait_time=5)
            for msg in received_msgs:
                print(f'Received message: {msg.body}')
                receiver.complete_message(msg)

if __name__ == '__main__':
    consume_event()