from __future__ import annotations

from typing import Any, Mapping, Optional

from messaging_client import get_sns_client, get_sns_topic_arn
from messaging_models import PublishResult, build_envelope


PROVIDER = "aws-sns"


def publish_event(event_type: str, payload: Mapping[str, Any] | str, attributes: Optional[Mapping[str, str]] = None, topic_arn: Optional[str] = None) -> PublishResult:
    client = get_sns_client()
    resolved_topic_arn = get_sns_topic_arn(topic_arn)
    envelope = build_envelope(event_type=event_type, payload=payload, attributes=attributes)
    response = client.publish(
        TopicArn=resolved_topic_arn,
        Message=envelope.to_json(),
        MessageAttributes={
            key: {"DataType": "String", "StringValue": value}
            for key, value in envelope.attributes.items()
        },
        Subject=event_type[:100],
    )
    return PublishResult(
        provider=PROVIDER,
        destination=resolved_topic_arn,
        message_id=response["MessageId"],
        status="published",
    )
