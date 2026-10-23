import os
from azure.servicebus import ServiceBusClient

def consume_event(queue_name):
    connection_str = os.getenv('SERVICE_BUS_CONNECTION_STR')
    with ServiceBusClient.from_connection_string(conn_str=connection_str) as client:
        receiver = client.get_queue_receiver(queue_name)
        with receiver:
            received_msgs = receiver.receive_messages(max_message_count=1, max_wait_time=5)
            for msg in received_msgs:
                print(str(msg))
                receiver.complete_message(msg)