import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from azure.servicebus import ServiceBusClient


@dataclass
class MessagingConfig:
    servicebus_connection_string: str
    topic_name: Optional[str]
    subscription_name: Optional[str]
    queue_name: Optional[str]
    dead_letter_queue_name: Optional[str]


def load_config() -> MessagingConfig:
    return MessagingConfig(
        servicebus_connection_string=os.environ["AZURE_SERVICEBUS_CONNECTION_STRING"],
        topic_name=os.getenv("AZURE_SERVICEBUS_TOPIC_NAME"),
        subscription_name=os.getenv("AZURE_SERVICEBUS_SUBSCRIPTION_NAME"),
        queue_name=os.getenv("AZURE_SERVICEBUS_QUEUE_NAME"),
        dead_letter_queue_name=os.getenv("AZURE_SERVICEBUS_DEAD_LETTER_QUEUE_NAME"),
    )


def create_servicebus_client() -> ServiceBusClient:
    return ServiceBusClient.from_connection_string(os.environ["AZURE_SERVICEBUS_CONNECTION_STRING"])


def normalize_message(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    return {"message": str(payload)}


def message_body_text(message: Any) -> str:
    body = getattr(message, "body", message)
    if isinstance(body, (bytes, bytearray)):
        return body.decode("utf-8")
    if isinstance(body, list):
        return b"".join(body).decode("utf-8")
    return str(body)
