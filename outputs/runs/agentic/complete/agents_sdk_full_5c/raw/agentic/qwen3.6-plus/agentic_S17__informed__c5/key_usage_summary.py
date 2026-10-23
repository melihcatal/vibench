"""
[LATER-STEP] key_usage_summary.py

Summarizes key usage and crypto events by querying AWS CloudTrail for AWS KMS API calls.
Provider: AWS CloudTrail / AWS KMS | SDK: boto3 | Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

Fetches CloudTrail events for KMS actions (Encrypt, Decrypt, GenerateDataKey, Sign, etc.)
and produces a usage summary per key ID.
"""

import os
import sys
import logging
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

# AWS KMS-relevant CloudTrail event names to track
KMS_EVENT_NAMES = [
    "Encrypt",
    "Decrypt",
    "GenerateDataKey",
    "GenerateDataKeyWithoutPlaintext",
    "ReEncrypt",
    "Sign",
    "Verify",
    "CreateKey",
    "ScheduleKeyDeletion",
    "DisableKey",
    "EnableKey",
    "DescribeKey",
]


def _build_cloudtrail_client() -> boto3.client:
    """Build an AWS CloudTrail client using environment credentials."""
    return boto3.client(
        "cloudtrail",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
    )


def fetch_kms_events(
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    max_results: int = 100,
    lookup_key_id: Optional[str] = None,
) -> List[dict]:
    """
    Fetch CloudTrail events for AWS KMS operations.

    Args:
        start_time: Start of the query window. Defaults to 24 hours ago.
        end_time: End of the query window. Defaults to now.
        max_results: Maximum events to retrieve per page.
        lookup_key_id: Optional KMS key ID to filter events.

    Returns:
        List of CloudTrail event dicts.
    """
    client = _build_cloudtrail_client()

    now = datetime.utcnow()
    if start_time is None:
        start_time = now - timedelta(hours=24)
    if end_time is None:
        end_time = now

    lookup_attributes = [
        {"AttributeKey": "EventSource", "AttributeValue": "kms.amazonaws.com"}
    ]
    if lookup_key_id:
        lookup_attributes.append(
            {"AttributeKey": "ResourceName", "AttributeValue": lookup_key_id}
        )

    events: List[dict] = []
    paginator = client.get_paginator("lookup_events")

    page_params = {
        "LookupAttributes": lookup_attributes,
        "StartTime": start_time,
        "EndTime": end_time,
        "MaxResults": max_results,
    }

    try:
        for page in paginator.paginate(**page_params):
            events.extend(page.get("Events", []))
            if "NextToken" not in page:
                break
            page_params["NextToken"] = page["NextToken"]
    except ClientError as exc:
        logger.error("CloudTrail lookup failed: %s", exc)
        return []

    return events


def summarize_key_usage(events: List[dict]) -> Dict[str, dict]:
    """
    Summarize KMS key usage from CloudTrail events.

    Returns a dict keyed by KMS key ID with operation counts, timestamps, etc.
    """
    summary: Dict[str, dict] = defaultdict(lambda: {
        "total_events": 0,
        "operations": defaultdict(int),
        "first_seen": None,
        "last_seen": None,
        "user_agents": set(),
        "source_ips": set(),
        "errors": 0,
    })

    for event in events:
        event_name = event.get("EventName", "Unknown")
        if event_name not in KMS_EVENT_NAMES:
            continue

        resource_list = event.get("Resources", [])
        key_id = "unknown"
        for res in resource_list:
            if res.get("ResourceType") == "AWS::KMS::Key":
                key_id = res.get("ResourceName", "unknown")
                break

        if key_id == "unknown" and "ResourceName" in event:
            key_id = event["ResourceName"]

        ts = event.get("EventTime")
        if isinstance(ts, datetime):
            ts_str = ts.isoformat()
        else:
            ts_str = str(ts)

        entry = summary[key_id]
        entry["total_events"] += 1
        entry["operations"][event_name] += 1

        if entry["first_seen"] is None:
            entry["first_seen"] = ts_str
        entry["last_seen"] = ts_str

        user_agent = event.get("UserAgent", "")
        if user_agent:
            entry["user_agents"].add(user_agent)

        source_ip = event.get("SourceIPAddress", "")
        if source_ip:
            entry["source_ips"].add(source_ip)

        error_code = event.get("ErrorCode", "")
        if error_code:
            entry["errors"] += 1

    # Convert sets to lists for JSON serializability
    result: Dict[str, dict] = {}
    for key_id, data in summary.items():
        result[key_id] = {
            "total_events": data["total_events"],
            "operations": dict(data["operations"]),
            "first_seen": data["first_seen"],
            "last_seen": data["last_seen"],
            "user_agents": sorted(data["user_agents"]),
            "source_ips": sorted(data["source_ips"]),
            "errors": data["errors"],
        }

    return result


def generate_key_usage_summary(
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    lookup_key_id: Optional[str] = None,
    max_results: int = 100,
) -> Dict[str, dict]:
    """
    Full pipeline: fetch KMS CloudTrail events and produce usage summary.

    Returns dict keyed by key ID with aggregated usage statistics.
    """
    events = fetch_kms_events(
        start_time=start_time,
        end_time=end_time,
        max_results=max_results,
        lookup_key_id=lookup_key_id,
    )
    return summarize_key_usage(events)


def main() -> None:
    """CLI entry point for generating key usage summary."""
    logging.basicConfig(level=logging.INFO)

    key_id = os.getenv("AWS_KMS_KEY_ID")
    summary = generate_key_usage_summary(lookup_key_id=key_id)

    for kid, data in summary.items():
        print(f"Key: {kid}")
        print(f"  Total events: {data['total_events']}")
        print(f"  Operations: {data['operations']}")
        print(f"  First seen: {data['first_seen']}")
        print(f"  Last seen: {data['last_seen']}")
        print(f"  Errors: {data['errors']}")
        print()


if __name__ == "__main__":
    main()
