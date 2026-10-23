from __future__ import annotations

import os
from dataclasses import asdict
from typing import Any, Dict, Iterable, List, Optional

from azure.servicebus import ServiceBusClient, ServiceBusMessage
from azure.servicebus.exceptions import ServiceBusError

from messaging_models import (
    BatchPublishRequest,
    BatchPublishResult,
    ConsumeResult,
    DeadLetterRecord,
    PublishEventRequest,
    PublishResult,
    normalize_payload_text,
)

PROVIDER_NAME = "Azure Service Bus"
ENV_CONNECTION_STRING = "AZURE_SERVICE_BUS_CONNECTION_STRING"


class MessagingClientError(RuntimeError):
    pass


class AzureServiceBusMessagingClient:
    def __init__(self, connection_string: Optional[str] = None):
        self.connection_string = connection_string or os.getenv(ENV_CONNECTION_STRING)
        if not self.connection_string:
            raise MessagingClientError(f"Missing {ENV_CONNECTION_STRING}")
        self._client = ServiceBusClient.from_connection_string(self.connection_string)

    def publish_event(self, request: PublishEventRequest) -> PublishResult:
        try:
            with self._client.get_topic_sender(request.topic) as sender:
                message = ServiceBusMessage(
                    normalize_payload_text(request.payload),
                    content_type="application/json",
                    application_properties=request.attributes or None,
                    message_id=request.message_id,
                )
                sender.send_messages(message)
            return PublishResult(message_id=request.message_id or "generated", provider=PROVIDER_NAME, topic=request.topic)
        except ServiceBusError as exc:
            raise MessagingClientError(str(exc)) from exc

    def batch_publish(self, request: BatchPublishRequest) -> BatchPublishResult:
        ids: List[str] = []
        try:
            with self._client.get_topic_sender(request.topic) as sender:
                batch = []
                for item in request.messages:
                    ids.append(item.message_id or "generated")
                    batch.append(
                        ServiceBusMessage(
                            normalize_payload_text(item.payload),
                            content_type="application/json",
                            application_properties=item.attributes or None,
                            message_id=item.message_id,
                        )
                    )
                sender.send_messages(batch)
            return BatchPublishResult(topic=request.topic, provider=PROVIDER_NAME, message_ids=ids)
        except ServiceBusError as exc:
            raise MessagingClientError(str(exc)) from exc

    def consume_one(self, subscription: str) -> ConsumeResult:
        try:
            with self._client.get_subscription_receiver(topic_name=subscription.split("/", 1)[0], subscription_name=subscription.split("/", 1)[1] if "/" in subscription else subscription) as receiver:
                messages = receiver.receive_messages(max_message_count=1, max_wait_time=5)
                msg = messages[0]
                payload = {"text": normalize_payload_text(msg.body)}
                return ConsumeResult(message_id=str(msg.message_id), provider=PROVIDER_NAME, subscription=subscription, payload=payload, attributes=dict(msg.application_properties or {}), ack_id=getattr(msg, "lock_token", None))
        except (ServiceBusError, IndexError) as exc:
            raise MessagingClientError(str(exc)) from exc

    def send_dead_letter(self, destination: str, record: DeadLetterRecord) -> None:
        try:
            with self._client.get_queue_sender(destination) as sender:
                sender.send_messages(
                    ServiceBusMessage(
                        normalize_payload_text(asdict(record)),
                        content_type="application/json",
                        application_properties=record.attributes or None,
                        message_id=record.source_subscription,
                    )
                )
        except ServiceBusError as exc:
            raise MessagingClientError(str(exc)) from exc
