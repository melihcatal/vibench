from __future__ import annotations

import os
from typing import Optional

from azure.servicebus import ServiceBusClient, ServiceBusMessage
from azure.servicebus.management import ServiceBusAdministrationClient


DEFAULT_QUEUE_ENV = "AZURE_SERVICE_BUS_QUEUE_NAME"
DEFAULT_DEAD_LETTER_QUEUE_ENV = "AZURE_SERVICE_BUS_DEAD_LETTER_QUEUE_NAME"
DEFAULT_CONNECTION_STRING_ENV = "AZURE_SERVICE_BUS_CONNECTION_STRING"


class MessagingConfig:
    def __init__(self) -> None:
        self.connection_string = os.environ[DEFAULT_CONNECTION_STRING_ENV]
        self.queue_name = os.environ.get(DEFAULT_QUEUE_ENV, "app-events")
        self.dead_letter_queue_name = os.environ.get(DEFAULT_DEAD_LETTER_QUEUE_ENV, "app-events-dead-letter")



def get_servicebus_client(config: Optional[MessagingConfig] = None) -> ServiceBusClient:
    cfg = config or MessagingConfig()
    return ServiceBusClient.from_connection_string(conn_str=cfg.connection_string, logging_enable=False)



def get_admin_client(config: Optional[MessagingConfig] = None) -> ServiceBusAdministrationClient:
    cfg = config or MessagingConfig()
    return ServiceBusAdministrationClient.from_connection_string(conn_str=cfg.connection_string)



def build_servicebus_message(body: str, *, message_id: Optional[str] = None, application_properties: Optional[dict] = None) -> ServiceBusMessage:
    return ServiceBusMessage(
        body,
        message_id=message_id,
        content_type="application/json",
        application_properties=application_properties or {},
    )
