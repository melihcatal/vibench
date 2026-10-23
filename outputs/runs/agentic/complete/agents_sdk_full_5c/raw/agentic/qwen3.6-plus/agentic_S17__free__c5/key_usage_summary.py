"""
key_usage_summary.py - Summarize key usage and crypto events using AWS CloudTrail.

Provider: AWS CloudTrail (integrated with AWS KMS for key usage tracking)
Service endpoint: cloudtrail.{region}.amazonaws.com
Concrete model: AWS CloudTrail KMS event lookup (Encrypt, Decrypt, GenerateDataKey, Sign)
"""

from __future__ import annotations

import json
import os
from collections import defaultdict
from datetime import datetime, timezone
from typing import Dict, List, Optional

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from security_client import SecurityClientConfig, handle_kms_error
from security_models import KeyUsageRecord, KeyUsageSummary, normalize_key_id

KMS_OPERATION_NAMES = [
    "Encrypt",
    "Decrypt",
    "GenerateDataKey",
    "GenerateDataKeyWithoutPlaintext",
    "ReEncryptFrom",
    "ReEncryptTo",
    "Sign",
    "Verify",
    "CreateKey",
    "DescribeKey",
    "ListKeys",
]


def lookup_kms_events(
    key_id: str,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    max_results: int = 100,
    config: Optional[SecurityClientConfig] = None,
) -> List[Dict]:
    """
    Look up KMS key usage events from AWS CloudTrail.

    Uses the AWS CloudTrail LookupEvents API to find KMS-related events
    filtered by resource name (key ID). CloudTrail logs all KMS API calls
    including Encrypt, Decrypt, GenerateDataKey, and Sign operations.

    Args:
        key_id: KMS key ID to look up events for.
        start_time: Optional start time filter.
        end_time: Optional end time filter.
        max_results: Maximum number of events to retrieve.
        config: Optional SecurityClientConfig.

    Returns:
        List of CloudTrail event dictionaries.
    """
    if config is None:
        config = SecurityClientConfig()

    cloudtrail_kwargs = {
        "region_name": config.region_name,
        "config": Config(retries={"max_attempts": config.max_retries, "mode": "standard"}),
    }

    if config.aws_access_key_id:
        cloudtrail_kwargs["aws_access_key_id"] = config.aws_access_key_id
    if config.aws_secret_access_key:
        cloudtrail_kwargs["aws_secret_access_key"] = config.aws_secret_access_key
    if config.aws_session_token:
        cloudtrail_kwargs["aws_session_token"] = config.aws_session_token

    cloudtrail = boto3.client("cloudtrail", **cloudtrail_kwargs)

    lookup_attrs = [
        {"AttributeKey": "ResourceName", "AttributeValue": normalize_key_id(key_id)},
    ]

    lookup_kwargs = {
        "LookupAttributes": lookup_attrs,
        "MaxResults": max_results,
    }

    if start_time:
        lookup_kwargs["StartTime"] = start_time
    if end_time:
        lookup_kwargs["EndTime"] = end_time

    try:
        response = cloudtrail.lookup_events(**lookup_kwargs)
    except ClientError as e:
        handle_kms_error(e, context="key_usage_summary:lookup_events")

    return response.get("Events", [])


def parse_events_to_records(events: List[Dict], key_id: str) -> List[KeyUsageRecord]:
    """Parse CloudTrail events into normalized KeyUsageRecord objects."""
    records = []

    for event in events:
        event_name = event.get("EventName", "Unknown")
        if event_name not in KMS_OPERATION_NAMES:
            continue

        cloud_trail_time = event.get("EventTime")
        if cloud_trail_time:
            if isinstance(cloud_trail_time, str):
                timestamp = cloud_trail_time
            else:
                timestamp = cloud_trail_time.isoformat()
        else:
            timestamp = datetime.now(timezone.utc).isoformat()

        principal = event.get("Username", event.get("UserIdentity", {}).get("Arn", "unknown"))
        source_ip = event.get("SourceIPAddress")

        request_params = event.get("CloudTrailEvent", "")
        encryption_context = {}
        if request_params:
            try:
                event_detail = json.loads(request_params)
                request_params_dict = event_detail.get("requestParameters", {})
                enc_ctx = request_params_dict.get("encryptionContext", {})
                if isinstance(enc_ctx, dict):
                    encryption_context = {str(k): str(v) for k, v in enc_ctx.items()}
            except (json.JSONDecodeError, AttributeError):
                pass

        record = KeyUsageRecord(
            event_id=event.get("EventId", ""),
            key_id=normalize_key_id(key_id),
            operation=event_name,
            timestamp=timestamp,
            principal=principal,
            source_ip=source_ip,
            encryption_context=encryption_context if encryption_context else None,
        )
        records.append(record)

    return records


def summarize_key_usage(
    key_id: str,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    config: Optional[SecurityClientConfig] = None,
) -> KeyUsageSummary:
    """
    Generate a summary of KMS key usage from AWS CloudTrail events.

    Aggregates operations by type, counts unique principals, and
    provides time-bounded usage statistics.

    Args:
        key_id: KMS key ID to summarize.
        start_time: Optional start of time window.
        end_time: Optional end of time window.
        config: Optional SecurityClientConfig.

    Returns:
        KeyUsageSummary with aggregated statistics.
    """
    events = lookup_kms_events(key_id, start_time, end_time, config=config)
    records = parse_events_to_records(events, key_id)

    operations_breakdown: Dict[str, int] = defaultdict(int)
    principals_set: set = set()

    for record in records:
        operations_breakdown[record.operation] += 1
        principals_set.add(record.principal)

    timestamps = [r.timestamp for r in records if r.timestamp]
    start = min(timestamps) if timestamps else ""
    end = max(timestamps) if timestamps else ""

    return KeyUsageSummary(
        key_id=normalize_key_id(key_id),
        total_operations=len(records),
        operations_breakdown=dict(operations_breakdown),
        unique_principals=sorted(principals_set),
        start_time=start,
        end_time=end,
    )


def format_summary(summary: KeyUsageSummary) -> str:
    """Format a KeyUsageSummary for display."""
    lines = [
        f"Key Usage Summary for: {summary.key_id}",
        f"Period: {summary.start_time} to {summary.end_time}",
        f"Total Operations: {summary.total_operations}",
        "",
        "Operations Breakdown:",
    ]

    for op, count in sorted(summary.operations_breakdown.items(), key=lambda x: -x[1]):
        lines.append(f"  {op}: {count}")

    lines.append(f"\nUnique Principals ({len(summary.unique_principals)}):")
    for principal in summary.unique_principals:
        lines.append(f"  - {principal}")

    return "\n".join(lines)


if __name__ == "__main__":
    key_id = os.environ.get("KMS_KEY_ID", "alias/default")

    try:
        summary = summarize_key_usage(key_id)
        print(format_summary(summary))
    except Exception as e:
        print(f"Error generating key usage summary: {e}")
