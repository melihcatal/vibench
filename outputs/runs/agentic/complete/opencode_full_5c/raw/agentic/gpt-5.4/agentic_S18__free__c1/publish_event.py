from __future__ import annotations

from messaging_client import sns_client, topic_arn
from messaging_models import EventMessage, PublishResult


def publish_event(message: EventMessage, subject: str | None = None) -> PublishResult:
    response = sns_client().publish(
        TopicArn=topic_arn(),
        Message=message.as_json(),
        Subject=subject or message.event_type,
        MessageAttributes={
            key: {"DataType": "String", "StringValue": value}
            for key, value in message.attributes.items()
        },
    )
    return PublishResult(
        provider="aws_sns",
        destination=topic_arn(),
        message_id=response["MessageId"],
    )
