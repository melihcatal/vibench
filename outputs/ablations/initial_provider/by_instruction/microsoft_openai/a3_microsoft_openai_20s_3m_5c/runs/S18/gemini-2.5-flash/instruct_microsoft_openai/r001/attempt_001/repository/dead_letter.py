import os
from azure.servicebus import ServiceBusReceiver
from messaging_client import get_service_bus_client
from messaging_models import EventMessage

# Configuration
SERVICE_BUS_TOPIC_NAME = os.environ.get("AZURE_SERVICE_BUS_TOPIC_NAME", "my_topic")
SERVICE_BUS_SUBSCRIPTION_NAME = os.environ.get("AZURE_SERVICE_BUS_SUBSCRIPTION_NAME", "my_subscription")

def send_to_dead_letter(reason: str = "ProcessingFailed", description: str = "Message failed custom validation"):
    client = None
    try:
        client = get_service_bus_client(topic_name=SERVICE_BUS_TOPIC_NAME, subscription_name=SERVICE_BUS_SUBSCRIPTION_NAME)
        receiver = client.get_receiver()

        with receiver:
            for msg in receiver: # Receive one message to dead-letter
                try:
                    event_message = EventMessage.from_json(str(msg.body))
                    print(f"Attempting to dead-letter event ID: {event_message.event_id}")
                    receiver.dead_letter_message(msg, reason=reason, error_description=description)
                    print(f"Event ID: {event_message.event_id} sent to dead-letter queue.")
                    return event_message
                except Exception as e:
                    print(f"Error processing message for dead-lettering: {e}")
                    # If even dead-lettering fails, complete or abandon based on policy
                    receiver.abandon_message(msg) 
                    return None
            print("No messages to dead-letter.")
            return None

    except Exception as e:
        print(f"Error setting up dead-letter operation: {e}")
        return None
    finally:
        if client:
            client.close()

if __name__ == "__main__":
    print("Attempting to receive and dead-letter an event...")
    dead_lettered_event = send_to_dead_letter("InvalidFormat", "The event payload was not in the expected JSON format.")
    if dead_lettered_event:
        print(f"Successfully initiated dead-letter for event: {dead_lettered_event.event_id}")
