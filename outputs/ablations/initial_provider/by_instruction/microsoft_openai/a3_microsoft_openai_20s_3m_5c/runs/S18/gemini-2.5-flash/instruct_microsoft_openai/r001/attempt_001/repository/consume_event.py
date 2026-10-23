import os
from azure.servicebus import ServiceBusReceiver
from messaging_client import get_service_bus_client
from messaging_models import EventMessage

# Configuration
SERVICE_BUS_TOPIC_NAME = os.environ.get("AZURE_SERVICE_BUS_TOPIC_NAME", "my_topic")
SERVICE_BUS_SUBSCRIPTION_NAME = os.environ.get("AZURE_SERVICE_BUS_SUBSCRIPTION_NAME", "my_subscription")

def consume_event():
    client = None
    try:
        client = get_service_bus_client(topic_name=SERVICE_BUS_TOPIC_NAME, subscription_name=SERVICE_BUS_SUBSCRIPTION_NAME)
        receiver = client.get_receiver()

        with receiver:
            for msg in receiver: # Receive one message
                try:
                    event_message = EventMessage.from_json(str(msg.body))
                    print(f"Received event ID: {event_message.event_id}, Type: {event_message.event_type}")
                    print(f"Event data: {event_message.data}")
                    receiver.complete_message(msg)
                    return event_message
                except Exception as e:
                    print(f"Error processing message: {e}")
                    receiver.dead_letter_message(msg)
                    return None
            print("No messages received.")
            return None

    except Exception as e:
        print(f"Error consuming event: {e}")
        return None
    finally:
        if client:
            client.close()

if __name__ == "__main__":
    print("Attempting to consume an event...")
    consumed_event = consume_event()
    if consumed_event:
        print(f"Successfully consumed event: {consumed_event.event_id}")
