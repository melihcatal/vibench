from __future__ import annotations

import os
from typing import Optional

from azure.servicebus import ServiceBusClient, ServiceBusMessage


SERVICE_BUS_CONNECTION_ENV = "AZURE_SERVICE_BUS_CONNECTION_STRING"
SERVICE_BUS_TOPIC_ENV = "AZURE_SERVICE_BUS_TOPIC"
SERVICE_BUS_SUBSCRIPTION_ENV = "AZURE_SERVICE_BUS_SUBSCRIPTION"
SERVICE_BUS_QUEUE_ENV = "AZURE_SERVICE_BUS_QUEUE"
SERVICE_BUS_DEAD_LETTER_QUEUE_ENV = "AZURE_SERVICE_BUS_DEAD_LETTER_QUEUE"


def get_connection_string() -> str:
    value = os.environ[SERVICE_BUS_CONNECTION_ENV]
    if not value:
        raise ValueError("Missing Azure Service Bus connection string")
    return value


def create_servicebus_client() -> ServiceBusClient:
    return ServiceBusClient.from_connection_string(conn_str=get_connection_string(), logging_enable=False)


def get_topic_name(explicit: Optional[str] = None) -> str:
    return explicit or os.environ[SERVICE_BUS_TOPIC_ENV]


def get_subscription_name(explicit: Optional[str] = None) -> str:
    return explicit or os.environ[SERVICE_BUS_SUBSCRIPTION_ENV]


def get_queue_name(explicit: Optional[str] = None) -> str:
    return explicit or os.environ[SERVICE_BUS_QUEUE_ENV]


def get_dead_letter_queue_name(explicit: Optional[str] = None) -> str:
    return explicit or os.environ.get(SERVICE_BUS_DEAD_LETTER_QUEUE_ENV, get_queue_name())


def build_servicebus_message(body: bytes, message_id: str, subject: Optional[str] = None, application_properties: Optional[dict] = None, content_type: str = "application/json") -> ServiceBusMessage:
    return ServiceBusMessage(
        body,
        message_id=message_id,
        subject=subject,
        application_properties=application_properties or {},
        content_type=content_type,
    )
