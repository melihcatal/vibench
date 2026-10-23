import os
import json
from typing import Dict, List, Any

# Azure Service Bus integration
CONN_STR = os.getenv("AZURE_SERVICE_BUS_CONNECTION_STRING")


def publish_batch(topic_name: str, events: List[Dict[str, Any]]) -> None:
    """Publish a batch of events to a Service Bus topic.
    Each event must include a unique ID.
    """
    from azure.servicebus import ServiceBusClient, ServiceBusMessage

    client = ServiceBusClient.from_connection_string(CONN_STR)
    sender = client.get_topic_sender(topic_name)
    messages = [ServiceBusMessage(json.dumps(ev)) for ev in events]
    sender.send_batch(messages)


# Example of adding a batch ID if missing
for ev in events:
    if "batch_id" not in ev:
        ev["batch_id"] = "batch-001"
