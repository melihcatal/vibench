from __future__ import annotations

import os
from typing import Any, Dict, Iterable, List, Optional

from azure.servicebus import ServiceBusClient, ServiceBusMessage
from azure.servicebus.exceptions import ServiceBusError

from messaging_models import MessagingConfig, MessageEnvelope, normalize_message_payload


def load_config() -> MessagingConfig:
    return MessagingConfig(
        provider="azure-servicebus",
        connection_string=os.getenv("AZURE_SERVICE_BUS_CONNECTION_STRING", ""),
        publish_target=os.getenv("AZURE_SERVICE_BUS_QUEUE_NAME", "messaging-publish-queue"),
        consume_target=os.getenv("AZURE_SERVICE_BUS_QUEUE_NAME", "messaging-publish-queue"),
        dead_letter_target=os.getenv("AZURE_SERVICE_BUS_DEAD_LETTER_QUEUE_NAME", "messaging-dead-letter-queue"),
        batch_target=os.getenv("AZURE_SERVICE_BUS_QUEUE_NAME", "messaging-publish-queue"),
    )


def create_client(config: Optional[MessagingConfig] = None) -> ServiceBusClient:
    cfg = config or load_config()
    if not cfg.connection_string:
        raise ValueError("AZURE_SERVICE_BUS_CONNECTION_STRING is required")
    return ServiceBusClient.from_connection_string(cfg.connection_string)


def send_to_queue(queue_name: str, envelope: MessageEnvelope, config: Optional[MessagingConfig] = None) -> str:
    client = create_client(config)
    with client:
        sender = client.get_queue_sender(queue_name=queue_name)
        with sender:
            message = ServiceBusMessage(
                envelope.to_json(),
                message_id=envelope.message_id,
                content_type="application/json",
                correlation_id=envelope.correlation_id,
                application_properties=envelope.attributes,
            )
            sender.send_messages(message)
    return envelope.message_id


def send_batch_to_queue(queue_name: str, envelopes: Iterable[MessageEnvelope], config: Optional[MessagingConfig] = None) -> List[str]:
    client = create_client(config)
    published: List[str] = []
    with client:
        sender = client.get_queue_sender(queue_name=queue_name)
        with sender:
            messages = []
            for envelope in envelopes:
                published.append(envelope.message_id)
                messages.append(
                    ServiceBusMessage(
                        envelope.to_json(),
                        message_id=envelope.message_id,
                        content_type="application/json",
                        correlation_id=envelope.correlation_id,
                        application_properties=envelope.attributes,
                    )
                )
            if messages:
                sender.send_messages(messages)
    return published


def receive_one(queue_name: str, config: Optional[MessagingConfig] = None) -> Dict[str, Any]:
    client = create_client(config)
    with client:
        receiver = client.get_queue_receiver(queue_name=queue_name, max_wait_time=5)
        with receiver:
            messages = receiver.receive_messages(max_message_count=1, max_wait_time=5)
            if not messages:
                return {"message_id": "", "body": {}, "delivery_count": 0}
            message = messages[0]
            body = normalize_message_payload(str(message))
            receiver.complete_message(message)
            return {
                "message_id": getattr(message, "message_id", ""),
                "body": body,
                "delivery_count": getattr(message, "delivery_count", 0),
            }


def dead_letter_message(queue_name: str, message: Any, reason: str, config: Optional[MessagingConfig] = None) -> str:
    client = create_client(config)
    with client:
        receiver = client.get_queue_receiver(queue_name=queue_name, max_wait_time=5)
        with receiver:
            if hasattr(message, "dead_letter"):
                receiver.dead_letter_message(message, reason=reason, error_description=reason)
                return getattr(message, "message_id", "")
    raise ServiceBusError(reason)
