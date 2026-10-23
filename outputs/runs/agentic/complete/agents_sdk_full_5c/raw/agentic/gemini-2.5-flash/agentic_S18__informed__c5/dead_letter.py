import os
import json
from azure.servicebus import ServiceBusClient, ServiceBusMessage
from messaging_client import get_service_bus_client

def send_to_dead_letter_destination(dead_letter_topic_or_queue_name: str, failed_message_data: dict, original_message_id: str = None):
    """Sends a failed message to a designated dead-letter topic or queue."""
    servicebus_client = get_service_bus_client()
    sender = servicebus_client.get_topic_sender(topic_name=dead_letter_topic_or_queue_name) if "_topic" in dead_letter_topic_or_queue_name else servicebus_client.get_queue_sender(queue_name=dead_letter_topic_or_queue_name)

    with sender:
        message_content = {
            "original_message_id": original_message_id,
            "failure_reason": "processing_failed",
            "original_payload": failed_message_data
        }
        message = ServiceBusMessage(json.dumps(message_content))
        if original_message_id:
            message.correlation_id = original_message_id
        sender.send_messages(message)
        print(f"Sent failed message to dead-letter destination '{dead_letter_topic_or_queue_name}': {message_content}")

if __name__ == '__main__':
    # Example usage (replace with actual dead-letter topic/queue name and failed message data)
    dlq_destination = os.environ.get("AZURE_SERVICE_BUS_DEAD_LETTER_DESTINATION", "my_dead_letter_queue")
    failed_data = {"id": "fail-456", "type": "payment_failed", "error": "invalid_card", "retries": 3}
    original_msg_id = "msg-original-789"
    send_to_dead_letter_destination(dlq_destination, failed_data, original_msg_id)
