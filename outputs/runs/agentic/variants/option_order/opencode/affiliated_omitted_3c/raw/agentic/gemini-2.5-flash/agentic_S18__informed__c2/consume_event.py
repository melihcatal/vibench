import os
from azure.servicebus import ServiceBusReceiveMode
from messaging_client import get_servicebus_client
from messaging_models import EventMessage


def consume_event(queue_name: str, max_wait_time: float = 5):
    client = get_servicebus_client()
    receiver = client.get_queue_receiver(
        queue_name=queue_name, receive_mode=ServiceBusReceiveMode.PEEK_LOCK
    )
    with receiver:
        received_messages = receiver.receive_messages(
            max_wait_time=max_wait_time, max_messages=1
        )
        if received_messages:
            message = received_messages[0]
            event = EventMessage.from_json_string(str(message.body))
            print(f"Received message: {event.message_id}, Payload: {event.payload}")
            message.complete()
            client.close()
            return event
        else:
            print("No messages received.")
            client.close()
            return None


if __name__ == "__main__":
    # Example usage
    queue_name = os.getenv("AZURE_SERVICE_BUS_QUEUE_NAME", "myqueue")
    print(f"Consuming event from {queue_name}...")
    consumed_event = consume_event(queue_name)
    if consumed_event:
        print(f"Successfully processed event with ID: {consumed_event.message_id}")
