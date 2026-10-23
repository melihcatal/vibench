import os
from azure.servicebus import ServiceBusClient
from messaging_client import MessagingClient
from messaging_models import EventMessage

def consume_event(topic_name: str, subscription_name: str):
    messaging_client = MessagingClient()
    servicebus_client = ServiceBusClient.from_connection_string(messaging_client.connection_str)

    with servicebus_client:        
        receiver = servicebus_client.get_subscription_receiver(topic_name=topic_name, subscription_name=subscription_name)
        with receiver:
            received_messages = receiver.receive_messages(max_messages=1, max_wait_time=5)
            for message in received_messages:
                print(f"Received message: {message.body.decode('utf-8')}")
                receiver.complete_message(message)
                return message.body.decode('utf-8')
            print("No messages received.")
            return None
