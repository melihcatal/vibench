import os
from azure.servicebus import ServiceBusReceiveMode
from messaging_client import get_servicebus_client, get_topic_name, get_subscription_name
from messaging_models import PubSubEvent

def dead_letter_message_example():
    client = get_servicebus_client()
    topic_name = get_topic_name()
    subscription_name = get_subscription_name()

    receiver = client.get_subscription_receiver(
        topic_name=topic_name,
        subscription_name=subscription_name,
        receive_mode=ServiceBusReceiveMode.PEEK_LOCK
    )

    with receiver:
        messages = receiver.receive_messages(max_wait_time=5, max_messages=1)
        if messages:
            for message in messages:
                try:
                    event = PubSubEvent.from_json(str(message))
                    print(f"Attempting to dead-letter event with ID: {event.id}")
                    # Simulate a processing failure and move to dead-letter queue
                    receiver.dead_letter_message(
                        message,
                        reason="SimulatedProcessingFailure",
                        error_description="Message failed validation or processing logic."
                    )
                    print(f"Event with ID: {event.id} dead-lettered.")
                except Exception as e:
                    print(f"Error processing message for dead-lettering: {e}")
                    # If there's an error even trying to dead-letter, we can log it.
        else:
            print("No messages available to dead-letter.")
    client.close()

if __name__ == "__main__":
    # Example usage: Ensure AZURE_SERVICEBUS_CONNECTION_STRING, AZURE_SERVICEBUS_TOPIC_NAME, and AZURE_SERVICEBUS_SUBSCRIPTION_NAME are set.
    dead_letter_message_example()
