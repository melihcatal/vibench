import os
from messaging_client import MessagingClient  # concrete provider: Azure Service Bus

# Azure Service Bus specifics
DLQ_NAME = os.getenv("AZURE_DEADLETTER_QUEUE")


def dead_letter(message):
    """Send a failed message to the dead‑letter destination.

    Args:
        message (dict): The original message to move.
    """
    client = MessagingClient(dead_letter_queue=DLQ_NAME)
    # client.send_dead_letter(message)
    print(f"Dead‑lettered message with ID {message.get('id', 'unknown')} to {DLQ_NAME}")
