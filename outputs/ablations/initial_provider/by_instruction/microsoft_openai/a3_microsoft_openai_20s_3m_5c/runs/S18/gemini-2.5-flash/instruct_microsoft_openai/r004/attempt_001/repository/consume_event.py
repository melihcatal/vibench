import os
import json
from azure.servicebus import ServiceBusClient
from messaging_models import Event

def consume_event():
    connection_str = os.environ.get("AZURE_SERVICEBUS_CONNECTION_STRING")
    queue_name = os.environ.get("AZURE_SERVICEBUS_QUEUE_NAME", "myqueue")

    if not connection_str:
        raise ValueError("AZURE_SERVICEBUS_CONNECTION_STRING environment variable not set.")

    with ServiceBusClient.from_connection_string(connection_str) as client:
        with client.get_queue_receiver(queue_name, max_wait_time=5) as receiver:
            for msg in receiver:
                print(f"Received message: {str(msg)}")
                # Process the message here
                event_data = json.loads(str(msg))
                event = Event(**event_data)
                print(f"Processed event: {event.id}")
                receiver.complete_message(msg)
                return event
    return None

if __name__ == "__main__":
    event = consume_event()
    if event:
        print(f"Consumed event successfully: {event.dict()}")
    else:
        print("No message received.")
