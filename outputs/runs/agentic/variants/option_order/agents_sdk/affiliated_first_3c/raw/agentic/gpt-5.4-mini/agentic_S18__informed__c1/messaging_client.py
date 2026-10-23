from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Optional
import os

from azure.servicebus import ServiceBusClient, ServiceBusMessage
from azure.servicebus.exceptions import ServiceBusError


@dataclass(frozen=True)
class MessagingConfig:
    connection_string: str
    topic_name: str
    subscription_name: str
    queue_name: str
    dead_letter_queue_name: str


@lru_cache(maxsize=1)
def load_config() -> MessagingConfig:
    connection_string = os.environ.get("AZURE_SERVICE_BUS_CONNECTION_STRING", "")
    topic_name = os.environ.get("AZURE_SERVICE_BUS_TOPIC_NAME", "events-topic")
    subscription_name = os.environ.get("AZURE_SERVICE_BUS_SUBSCRIPTION_NAME", "events-subscription")
    queue_name = os.environ.get("AZURE_SERVICE_BUS_QUEUE_NAME", "events-queue")
    dead_letter_queue_name = os.environ.get("AZURE_SERVICE_BUS_DEAD_LETTER_QUEUE_NAME", "events-dead-letter")
    if not connection_string:
        raise RuntimeError("AZURE_SERVICE_BUS_CONNECTION_STRING is required")
    return MessagingConfig(connection_string, topic_name, subscription_name, queue_name, dead_letter_queue_name)


@lru_cache(maxsize=1)
def get_client() -> ServiceBusClient:
    return ServiceBusClient.from_connection_string(load_config().connection_string)


def build_message(body: str, message_id: str, content_type: str = "application/json", **properties: str) -> ServiceBusMessage:
    msg = ServiceBusMessage(body)
    msg.message_id = message_id
    msg.content_type = content_type
    for key, value in properties.items():
        msg.application_properties[key] = value
    return msg


def close_client() -> None:
    client = get_client()
    try:
        client.close()
    except ServiceBusError:
        pass
