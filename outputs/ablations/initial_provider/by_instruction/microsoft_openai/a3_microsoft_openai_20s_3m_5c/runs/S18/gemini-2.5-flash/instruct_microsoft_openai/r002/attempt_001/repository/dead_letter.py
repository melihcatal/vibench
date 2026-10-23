from azure.servicebus import ServiceBusClient, ServiceBusReceivedMessage
import os

def send_to_dead_letter(message: ServiceBusReceivedMessage, topic_name: str, subscription_name: str, reason: str, description: str):
    """
    Sends a failed message to the dead-letter queue of an Azure Service Bus subscription.
    """
    connection_str = os.environ.get("AZURE_SERVICEBUS_CONNECTION_STRING")
    if not connection_str:
        raise ValueError("AZURE_SERVICEBUS_CONNECTION_STRING environment variable not set.")

    with ServiceBusClient.from_connection_string(connection_str) as client:
        receiver = client.get_subscription_receiver(topic_name=topic_name, subscription_name=subscription_name)
        with receiver:
            receiver.dead_letter_message(message, dead_letter_reason=reason, dead_letter_error_description=description)
            print(f"Message dead-lettered with reason: {reason}")

if __name__ == "__main__":
    # This is a conceptual example. In a real scenario, you'd have a received message object.
    # For demonstration purposes, we'll simulate a message.
    # To test this, you would typically consume a message first, then decide to dead-letter it.
    print("To test dead_letter.py, you need to first consume a message and then call send_to_dead_letter with the received message object.")
    print("Example: message_to_dl = ServiceBusReceivedMessage(body='{\"id\":\"test_dl\"}'.encode('utf-8'))")
    # send_to_dead_letter(message_to_dl, "my_topic", "my_subscription", "ProcessingFailed", "Message could not be processed due to invalid format.")
