from __future__ import annotations

from typing import Dict

from messaging_client import event_to_sqs_message, get_queue_url, sqs_client
from messaging_models import MessageEvent, PublishResult


def publish_event(event: MessageEvent, queue_url: str | None = None) -> PublishResult:
    client = sqs_client()
    destination = queue_url or get_queue_url("AWS_SQS_QUEUE_URL")
    message = event_to_sqs_message(event)
    response = client.send_message(QueueUrl=destination, **message)
    return PublishResult(
        message_id=response["MessageId"],
        destination=destination,
        attributes=event.attributes,
    )
