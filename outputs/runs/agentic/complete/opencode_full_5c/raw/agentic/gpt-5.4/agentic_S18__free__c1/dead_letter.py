from __future__ import annotations

from messaging_client import dead_letter_queue_url, sqs_client
from messaging_models import EventMessage, PublishResult


def send_to_dead_letter(message: EventMessage, failure_reason: str) -> PublishResult:
    response = sqs_client().send_message(
        QueueUrl=dead_letter_queue_url(),
        MessageBody=message.as_json(),
        MessageAttributes={
            "failure_reason": {"DataType": "String", "StringValue": failure_reason},
            **{
                key: {"DataType": "String", "StringValue": value}
                for key, value in message.attributes.items()
            },
        },
    )
    return PublishResult(
        provider="aws_sqs_dlq",
        destination=dead_letter_queue_url(),
        message_id=response["MessageId"],
    )
