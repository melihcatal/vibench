import os
from azure.servicebus import ServiceBusClient, ServiceBusMessage
from messaging_client import MessagingClient

def send_to_dead_letter(topic_name: str, subscription_name: str, original_message_body: str, dead_letter_reason: str, dead_letter_error_description: str):
    messaging_client = MessagingClient()
    servicebus_client = ServiceBusClient.from_connection_string(messaging_client.connection_str)

    # This is a conceptual example. In a real scenario, you'd move a *received* message to dead-letter.
    # For this example, we'll simulate sending a new message directly to a dead-letter queue if it existed,
    # or simply marking a message as dead-lettered during processing by calling receiver.dead_letter_message().
    # Azure Service Bus automatically handles the dead-letter queue when dead_letter_message is called on a received message.
    # Here we'll just print the action as we don't have a live message to dead-letter within this isolated script.
    
    print(f"Simulating sending message to dead-letter for topic/subscription: {topic_name}/{subscription_name}")
    print(f"Original Message: {original_message_body}")
    print(f"Dead-Letter Reason: {dead_letter_reason}")
    print(f"Dead-Letter Error Description: {dead_letter_error_description}")

    # To actually dead-letter a *received* message, you would do something like:
    # with servicebus_client.get_subscription_receiver(topic_name=topic_name, subscription_name=subscription_name) as receiver:
    #     received_messages = receiver.receive_messages(max_messages=1)
    #     for message in received_messages:
    #         receiver.dead_letter_message(message, reason=dead_letter_reason, error_description=dead_letter_error_description)
    #         print(f"Message {message.message_id} dead-lettered.")

