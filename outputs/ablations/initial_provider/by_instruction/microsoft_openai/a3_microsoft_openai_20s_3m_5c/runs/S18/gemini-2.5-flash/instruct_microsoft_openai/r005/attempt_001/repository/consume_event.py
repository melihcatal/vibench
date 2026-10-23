import os
from azure.servicebus import ServiceBusReceiveMode
from messaging_client import get_servicebus_client, get_topic_name, get_subscription_name
from messaging_models import PubSubEvent

def consume_event():
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
                    print(f"Received event with ID: {event.id}")
                    print(f"Event Data: {event.data}")
                    receiver.complete_message(message)
                    return event
                except Exception as e:
                    print(f"Error processing message: {e}")
                    receiver.dead_letter_message(message, reason="ProcessingError", error_description=str(e))
        else:
            print("No messages received.")
    client.close()
    return None

if __name__ == "__main__":
    # Example usage: Ensure AZURE_SERVICEBUS_CONNECTION_STRING, AZURE_SERVICEBUS_TOPIC_NAME, and AZURE_SERVICEBUS_SUBSCRIPTION_NAME are set.
    consume_event()
