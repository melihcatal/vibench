from __future__ import annotations

from messaging_client import get_queue_url, serialize_attributes, sqs_client
from messaging_models import ConsumedMessage, PublishResult
import json


def send_to_dead_letter(
    message: ConsumedMessage, reason: str, dead_letter_queue_url: str | None = None
) -> PublishResult:
    client = sqs_client()
    destination = dead_letter_queue_url or get_queue_url(
        "AWS_SQS_DEAD_LETTER_QUEUE_URL"
    )
    payload = {
        "failed_message_id": message.message_id,
        "reason": reason,
        "body": message.body,
        "attributes": message.attributes,
        "source_queue_url": message.queue_url,
    }
    response = client.send_message(
        QueueUrl=destination,
        MessageBody=json.dumps(payload, separators=(",", ":"), ensure_ascii=False),
        MessageAttributes=serialize_attributes(
            {"dead_letter_reason": reason, **message.attributes}
        ),
    )
    return PublishResult(
        message_id=response["MessageId"],
        destination=destination,
        attributes={"dead_letter_reason": reason},
    )
