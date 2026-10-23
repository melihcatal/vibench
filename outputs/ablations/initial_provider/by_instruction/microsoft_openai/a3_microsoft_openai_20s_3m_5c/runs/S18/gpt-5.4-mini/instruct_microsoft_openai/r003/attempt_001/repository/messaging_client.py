import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from azure.servicebus import ServiceBusClient


@dataclass
class MessagingConfig:
    connection_string: str
    queue_name: str
    dead_letter_queue_name: str
    batch_queue_name: str


def load_config() -> MessagingConfig:
    return MessagingConfig(
        connection_string=os.environ["AZURE_SERVICEBUS_CONNECTION_STRING"],
        queue_name=os.getenv("AZURE_SERVICEBUS_QUEUE_NAME", "events"),
        dead_letter_queue_name=os.getenv("AZURE_SERVICEBUS_DEAD_LETTER_QUEUE_NAME", "events-dlq"),
        batch_queue_name=os.getenv("AZURE_SERVICEBUS_BATCH_QUEUE_NAME", "events-batch"),
    )


def create_client() -> ServiceBusClient:
    return ServiceBusClient.from_connection_string(os.environ["AZURE_SERVICEBUS_CONNECTION_STRING"])


def build_message_props(message_id: Optional[str] = None, attributes: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    props = dict(attributes or {})
    if message_id:
        props["message_id"] = message_id
    return props
