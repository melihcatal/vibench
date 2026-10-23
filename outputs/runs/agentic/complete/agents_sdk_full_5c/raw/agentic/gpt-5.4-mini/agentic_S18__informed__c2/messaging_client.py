from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

from azure.servicebus import ServiceBusClient, ServiceBusMessage, ServiceBusReceiveMode
from azure.servicebus.exceptions import ServiceBusError

from messaging_models import MessageEnvelope, MessageResult, normalize_message_body


@dataclass(frozen=True)
class MessagingConfig:
    connection_string: str
    queue_name: str
    dead_letter_queue_name: str | None = None


def load_config() -> MessagingConfig:
    connection_string = os.environ["AZURE_SERVICE_BUS_CONNECTION_STRING"]
    queue_name = os.getenv("AZURE_SERVICE_BUS_QUEUE_NAME", "events")
    dead_letter_queue_name = os.getenv("AZURE_SERVICE_BUS_DEAD_LETTER_QUEUE_NAME", "events-dlq")
    return MessagingConfig(
        connection_string=connection_string,
        queue_name=queue_name,
        dead_letter_queue_name=dead_letter_queue_name,
    )


class AzureServiceBusMessagingClient:
    def __init__(self, config: MessagingConfig | None = None):
        self.config = config or load_config()
        self._client = ServiceBusClient.from_connection_string(self.config.connection_string)

    def publish_event(self, envelope: MessageEnvelope) -> MessageResult:
        try:
            with self._client:
                with self._client.get_queue_sender(queue_name=self.config.queue_name) as sender:
                    msg = ServiceBusMessage(
                        envelope.to_json(),
                        message_id=envelope.message_id,
                        content_type="application/json",
                        application_properties=envelope.attributes,
                    )
                    sender.send_messages(msg)
            return MessageResult(ok=True, provider="azure-servicebus", message_id=envelope.message_id)
        except ServiceBusError as exc:
            return MessageResult(ok=False, provider="azure-servicebus", message_id=envelope.message_id, detail=str(exc))

    def publish_batch(self, envelopes: list[MessageEnvelope]) -> list[MessageResult]:
        results: list[MessageResult] = []
        try:
            with self._client:
                with self._client.get_queue_sender(queue_name=self.config.queue_name) as sender:
                    batch = sender.create_message_batch()
                    for envelope in envelopes:
                        msg = ServiceBusMessage(
                            envelope.to_json(),
                            message_id=envelope.message_id,
                            content_type="application/json",
                            application_properties=envelope.attributes,
                        )
                        if not batch.try_add_message(msg):
                            sender.send_messages(batch)
                            batch = sender.create_message_batch()
                            batch.try_add_message(msg)
                        results.append(MessageResult(ok=True, provider="azure-servicebus", message_id=envelope.message_id))
                    if len(batch) > 0:
                        sender.send_messages(batch)
        except ServiceBusError as exc:
            return [MessageResult(ok=False, provider="azure-servicebus", detail=str(exc)) for _ in envelopes]
        return results

    def consume_one(self) -> dict[str, Any] | None:
        with self._client:
            with self._client.get_queue_receiver(queue_name=self.config.queue_name, receive_mode=ServiceBusReceiveMode.PEEK_LOCK) as receiver:
                messages = receiver.receive_messages(max_message_count=1, max_wait_time=10)
                if not messages:
                    return None
                message = messages[0]
                payload = normalize_message_body(str(message))
                receiver.complete_message(message)
                return {
                    "message_id": message.message_id,
                    "body": payload,
                    "application_properties": dict(message.application_properties or {}),
                }

    def dead_letter(self, reason: str, description: str, body: Any) -> MessageResult:
        target = self.config.dead_letter_queue_name or self.config.queue_name
        try:
            with self._client:
                with self._client.get_queue_sender(queue_name=target) as sender:
                    msg = ServiceBusMessage(
                        normalize_message_body(body),
                        content_type="application/json",
                        application_properties={"dead_letter_reason": reason, "dead_letter_description": description},
                    )
                    sender.send_messages(msg)
            return MessageResult(ok=True, provider="azure-servicebus", detail=reason)
        except ServiceBusError as exc:
            return MessageResult(ok=False, provider="azure-servicebus", detail=str(exc))
