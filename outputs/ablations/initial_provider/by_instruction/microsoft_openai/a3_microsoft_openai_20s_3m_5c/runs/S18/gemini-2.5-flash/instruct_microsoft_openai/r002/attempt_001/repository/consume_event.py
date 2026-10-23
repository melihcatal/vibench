from azure.servicebus import ServiceBusClient
import os
import json

def consume_event(topic_name: str, subscription_name: str):
    """
    Consumes one message from an Azure Service Bus subscription.
    """
    connection_str = os.environ.get("AZURE_SERVICEBUS_CONNECTION_STRING")
    if not connection_str:
        raise ValueError("AZURE_SERVICEBUS_CONNECTION_STRING environment variable not set.")

    with ServiceBusClient.from_connection_string(connection_str) as client:
        receiver = client.get_subscription_receiver(topic_name=topic_name, subscription_name=subscription_name)
        with receiver:
            messages = receiver.receive_messages(max_wait_time=5, max_messages=1)
            if messages:
                for message in messages:
                    body = str(message.body)
                    print(f"Received message: {body}")
                    # Complete the message to remove it from the subscription
                    receiver.complete_message(message)
                    return json.loads(body)
            else:
                print("No messages received.")
    return None

if __name__ == "__main__":
    # Example usage
    # Ensure AZURE_SERVICEBUS_CONNECTION_STRING, AZURE_SERVICEBUS_TOPIC_NAME, and AZURE_SERVICEBUS_SUBSCRIPTION_NAME are set
    topic = os.environ.get("AZURE_SERVICEBUS_TOPIC_NAME", "my_topic")
    subscription = os.environ.get("AZURE_SERVICEBUS_SUBSCRIPTION_NAME", "my_subscription")
    consume_event(topic, subscription)
