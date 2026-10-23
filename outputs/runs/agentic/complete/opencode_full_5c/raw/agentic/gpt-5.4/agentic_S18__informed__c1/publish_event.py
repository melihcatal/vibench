from __future__ import annotations

from typing import Any

from messaging_client import publish_to_topic
from messaging_models import PublishEventRequest, normalize_payload


def publish_event(
    topic_arn: str,
    payload: dict[str, Any] | str,
    subject: str | None = None,
    attributes: dict[str, str] | None = None,
) -> dict[str, Any]:
    request = PublishEventRequest(
        topic_arn=topic_arn,
        payload=normalize_payload(payload),
        subject=subject,
        attributes=attributes or {},
    )
    response = publish_to_topic(request)
    return {
        "provider": "aws_sns",
        "topic_arn": topic_arn,
        "message_id": response.get("MessageId"),
        "sequence_number": response.get("SequenceNumber"),
    }
