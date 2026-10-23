import os
import json
from azure.servicebus import ServiceBusClient
from messaging_client import get_service_bus_client

def consume_event(topic_name: str, subscription_name: str):
    """Consumes one message from an Azure Service Bus subscription."""
    servicebus_client = get_service_bus_client()
    receiver = servicebus_client.get_subscription_receiver(topic_name=topic_name, subscription_name=subscription_name)

    with receiver:
        received_msgs = receiver.receive_messages(max_messages=1, max_wait_time=5)
        if received_msgs:
            for msg in received_msgs:
                print(f"Received message: {str(msg)}")
                # Process the message
                try:
                    message_body = json.loads(str(msg))
                    print(f"Processed message body: {message_body}")
                    receiver.complete_message(msg)
                    return message_body
                except json.JSONDecodeError:
                    print(f"Could not decode message as JSON: {str(msg)}")
                    # Decide whether to complete, abandon, or dead-letter non-JSON messages
                    receiver.abandon_message(msg) # Abandon for now
        else:
            print("No messages received.")
    return None

if __name__ == '__main__':
    # Example usage (replace with actual topic and subscription names)
    topic = os.environ.get("AZURE_SERVICE_BUS_TOPIC_NAME", "my_topic")
    subscription = os.environ.get("AZURE_SERVICE_BUS_SUBSCRIPTION_NAME", "my_subscription")
    consumed = consume_event(topic, subscription)
    if consumed:
        print(f"Successfully consumed: {consumed}")
