from __future__ import annotations

from typing import Iterable, List

from security_client import cloudtrail_client, openai_client
from security_models import KeyUsageSummary


MODEL = "gpt-4o-mini"
KMS_EVENT_NAMES = ["Encrypt", "Decrypt", "GenerateDataKey", "Sign", "Verify"]


def fetch_kms_events(lookup_attribute_value: str, max_results: int = 25) -> List[dict]:
    client = cloudtrail_client()
    paginator = client.get_paginator("lookup_events")
    events: List[dict] = []
    for page in paginator.paginate(
        LookupAttributes=[{"AttributeKey": "ResourceName", "AttributeValue": lookup_attribute_value}],
        PaginationConfig={"MaxItems": max_results},
    ):
        for event in page.get("Events", []):
            if event.get("EventName") in KMS_EVENT_NAMES:
                events.append(event)
    return events[:max_results]


def summarize_key_usage(key_id: str) -> KeyUsageSummary:
    events = fetch_kms_events(key_id)
    client = openai_client()
    prompt = {
        "task": "Summarize AWS KMS key usage and crypto events for auditors.",
        "key_id": key_id,
        "events": [
            {
                "event_name": e.get("EventName"),
                "event_time": str(e.get("EventTime")),
                "username": e.get("Username"),
                "resources": e.get("Resources", []),
            }
            for e in events
        ],
    }
    response = client.responses.create(
        model=MODEL,
        input=[
            {"role": "system", "content": "You summarize AWS KMS usage for security reviewers in concise bullet points."},
            {"role": "user", "content": str(prompt)},
        ],
    )
    text = response.output_text
    highlights = [line.strip("- ") for line in text.splitlines() if line.strip().startswith("-")]
    return KeyUsageSummary(provider="openai", model=MODEL, summary=text, highlights=highlights)
