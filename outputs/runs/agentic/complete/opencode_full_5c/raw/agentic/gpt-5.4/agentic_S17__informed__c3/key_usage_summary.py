from __future__ import annotations

from typing import Iterable, Optional

from openai.types.chat import (
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)

from security_client import aws_cloudtrail_client, openai_client
from security_models import KeyUsageSummary


def _normalize_events(events: Iterable[dict], key_id: Optional[str]) -> list[dict]:
    normalized = []
    for event in events:
        resources = event.get("Resources") or []
        if key_id and not any(
            resource.get("ResourceName") == key_id for resource in resources
        ):
            continue
        normalized.append(
            {
                "event_name": event.get("EventName"),
                "event_time": str(event.get("EventTime")),
                "username": event.get("Username"),
                "resource_names": [
                    resource.get("ResourceName")
                    for resource in resources
                    if resource.get("ResourceName")
                ],
            }
        )
    return normalized


def key_usage_summary(
    lookup_days: int = 7, key_id: Optional[str] = None
) -> KeyUsageSummary:
    cloudtrail = aws_cloudtrail_client()
    attributes = [
        {"AttributeKey": "EventSource", "AttributeValue": "kms.amazonaws.com"}
    ]
    events = cloudtrail.lookup_events(LookupAttributes=attributes, MaxResults=50).get(
        "Events", []
    )
    normalized = _normalize_events(events, key_id)
    operations = sorted(
        {event["event_name"] for event in normalized if event.get("event_name")}
    )
    client = openai_client()
    messages: list[
        ChatCompletionSystemMessageParam | ChatCompletionUserMessageParam
    ] = [
        {
            "role": "system",
            "content": "Summarize AWS KMS key usage and crypto events concisely.",
        },
        {
            "role": "user",
            "content": f"Days: {lookup_days}\nKey: {key_id or 'all'}\nEvents: {normalized}",
        },
    ]
    completion = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        temperature=0,
    )
    summary = completion.choices[0].message.content or ""
    return KeyUsageSummary(
        provider="aws-cloudtrail+openai",
        key_id=key_id,
        event_count=len(normalized),
        operations=operations,
        summary=summary,
    )
