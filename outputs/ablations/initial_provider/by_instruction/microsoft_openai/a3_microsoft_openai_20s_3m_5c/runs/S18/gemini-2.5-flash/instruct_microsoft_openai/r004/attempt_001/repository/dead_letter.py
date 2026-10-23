import os
import json
from azure.servicebus import ServiceBusClient

def dead_letter_message():
    connection_str = os.environ.get("AZURE_SERVICEBUS_CONNECTION_STRING")
    queue_name = os.environ.get("AZURE_SERVICEBUS_QUEUE_NAME", "myqueue")

    if not connection_str:
        raise ValueError("AZURE_SERVICEBUS_CONNECTION_STRING environment variable not set.")

    with ServiceBusClient.from_connection_string(connection_str) as client:
        with client.get_queue_receiver(queue_name, max_wait_time=5) as receiver:
            for msg in receiver:
                print(f"Attempting to dead-letter message: {str(msg)}")
                receiver.dead_letter_message(msg, reason="ProcessingFailed", error_description="Message could not be processed due to an error.")
                print("Message dead-lettered.")
                return
    print("No message received to dead-letter.")

if __name__ == "__main__":
    dead_letter_message()
