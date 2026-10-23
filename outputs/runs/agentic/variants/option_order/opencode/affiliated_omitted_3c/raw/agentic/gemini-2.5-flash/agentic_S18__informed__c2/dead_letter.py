import os
from azure.servicebus import ServiceBusReceiveMode
from messaging_client import get_servicebus_client
from messaging_models import EventMessage


def send_to_dead_letter(
    queue_name: str,
    message_id: str,
    dead_letter_reason: str,
    dead_letter_error_description: str,
):
    client = get_servicebus_client()
    receiver = client.get_queue_receiver(
        queue_name=queue_name, receive_mode=ServiceBusReceiveMode.PEEK_LOCK
    )
    with receiver:
        # In a real scenario, you would likely have the actual ServiceBusReceivedMessage object
        # that failed to process. For this example, we simulate by receiving and then dead-lettering.
        received_messages = receiver.receive_messages(max_wait_time=5, max_messages=1)
        if received_messages:
            message = received_messages[0]
            if (
                EventMessage.from_json_string(str(message.body)).message_id
                == message_id
            ):
                message.dead_letter(
                    reason=dead_letter_reason,
                    error_description=dead_letter_error_description,
                )
                print(f"Message {message_id} sent to dead-letter queue.")
            else:
                print(
                    f"Message {message_id} not found for dead-lettering. Completing received message."
                )
                message.complete()
        else:
            print(
                f"No messages available in {queue_name} to dead-letter (simulated for message_id: {message_id})."
            )
    client.close()


if __name__ == "__main__":
    # Example usage
    queue_name = os.getenv("AZURE_SERVICE_BUS_QUEUE_NAME", "myqueue")
    failed_message_id = "123"
    print(
        f"Attempting to send message {failed_message_id} to dead-letter in {queue_name}..."
    )
    send_to_dead_letter(
        queue_name,
        failed_message_id,
        "ProcessingError",
        "Failed to process due to business logic error.",
    )
