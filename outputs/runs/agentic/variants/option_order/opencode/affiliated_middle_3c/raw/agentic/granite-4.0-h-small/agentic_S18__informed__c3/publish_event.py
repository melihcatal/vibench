import os
import json
from typing import Dict, List

# Azure Service Bus integration
# Environment variable used for connection string
CONN_STR = os.getenv("AZURE_SERVICE_BUS_CONNECTION_STRING")


def publish_event(topic_name: str, event: Dict[str, Any]) -> None:
    """Publish a single JSON event to the specified Service Bus topic.
    Requires AZURE_SERVICE_BUS_CONNECTION_STRING env var.
    """
    from azure.servicebus import ServiceBusClient, ServiceBusMessage

    client = ServiceBusClient.from_connection_string(CONN_STR)
    sender = client.get_topic_sender(topic_name)
    message = ServiceBusMessage(json.dumps(event))
    sender.send_messages(message)


def consume_event(subscription_name: str) -> Dict[str, Any]:
    """Consume one message from the given Service Bus subscription.
    Returns the deserialized JSON payload.
    """
    from azure.servicebus import ServiceBusClient, ServiceBusProcessor

    def on_message_received(msg_data):
        message = msg_data.message
        payload = json.loads(message.body)
        # Complete the message after processing
        message.complete()
        return payload

    def on_error(context):
        print("Error received: ", context)

    client = ServiceBusClient.from_connection_string(CONN_STR)
    processor = ServiceBusProcessor(
        client=client,
        topic_name=topic_name,
        subscription_name=subscription_name,
        message_handler=on_message_received,
        error_handler=on_error,
    )
    processor.start()
    try:
        payload = processor.receive_messages(max_wait_time=10)
        return next(payload, {})
    finally:
        processor.stop()


def send_to_dead_letter(topic_name: str, subscription_name: str, event: Dict[str, Any]):
    """Send a failed event to the dead-letter queue."""
    from azure.servicebus import ServiceBusClient, ServiceBusMessage

    client = ServiceBusClient.from_connection_string(CONN_STR)
    sender = client.get_topic_sender(topic_name)
    dlq_sender = client.get_dead_letter_sender(topic_name, subscription_name)
    dlq_message = ServiceBusMessage(
        json.dumps(event), message_annotations={"dlq": True}
    )
    dlq_sender.send_messages(dlq_message)


def batch_publish(topic_name: str, events: List[Dict[str, Any]]) -> None:
    """Publish a batch of events, each with a unique ID."""
    from azure.servicebus import ServiceBusClient

    client = ServiceBusClient.from_connection_string(CONN_STR)
    sender = client.get_topic_sender(topic_name)
    messages = [ServiceBusMessage(json.dumps(e)) for e in events]
    # Using send_batch
    sender.send_batch(messages)
