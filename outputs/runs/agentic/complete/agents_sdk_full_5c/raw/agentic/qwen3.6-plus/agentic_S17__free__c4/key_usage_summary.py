"""
Summarize key usage and crypto events using AWS CloudTrail via boto3.
Queries CloudTrail lookup events for AWS KMS operations and produces
structured summaries of key usage patterns.

Provider: AWS CloudTrail (boto3) - cloudtrail.us-east-1.amazonaws.com
"""

import json
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional, List, Dict, Any
from collections import defaultdict

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from security_models import KeyUsageEvent, KeyUsageSummary

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# AWS KMS event name patterns tracked in CloudTrail
KMS_EVENT_NAMES = [
    "Encrypt",
    "Decrypt",
    "GenerateDataKey",
    "GenerateDataKeyPair",
    "Sign",
    "Verify",
    "DescribeKey",
    "CreateKey",
    "DisableKey",
    "EnableKey",
    "ScheduleKeyDeletion",
    "ReEncrypt",
    "GenerateRandom",
]


def create_cloudtrail_client(region: str = "us-east-1") -> boto3.client:
    """
    Create a boto3 CloudTrail client for querying KMS usage events.
    Provider: AWS CloudTrail - cloudtrail.us-east-1.amazonaws.com
    """
    return boto3.client(
        "cloudtrail",
        region_name=region,
        config=Config(retries={"max_attempts": 3}, read_timeout=30),
    )


def lookup_kms_events(
    key_id: str = "",
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    region: str = "us-east-1",
    max_results: int = 50,
) -> List[Dict[str, Any]]:
    """
    Lookup AWS KMS events from CloudTrail.

    Provider: AWS CloudTrail (boto3) - cloudtrail.us-east-1.amazonaws.com

    Args:
        key_id: Filter by specific KMS key ID.
        start_time: Start of time range.
        end_time: End of time range.
        region: AWS region.
        max_results: Maximum number of events to return.

    Returns:
        List of CloudTrail event dicts.
    """
    ct_client = create_cloudtrail_client(region)
    events = []

    lookup_attributes = []
    if key_id:
        lookup_attributes.append(
            {"AttributeKey": "ResourceName", "AttributeValue": key_id}
        )

    params = {
        "LookupAttributes": lookup_attributes,
        "MaxResults": max_results,
    }
    if start_time:
        params["StartTime"] = start_time
    if end_time:
        params["EndTime"] = end_time

    try:
        logger.info("Looking up KMS events in CloudTrail for key %s", key_id or "all keys")
        response = ct_client.lookup_events(**params)
        events.extend(response.get("Events", []))

        # Paginate if needed
        while "NextToken" in response and len(events) < max_results:
            params["NextToken"] = response["NextToken"]
            response = ct_client.lookup_events(**params)
            events.extend(response.get("Events", []))

        # Filter to only KMS events
        kms_events = [
            e for e in events
            if e.get("EventSource") == "kms.amazonaws.com"
            or e.get("EventName") in KMS_EVENT_NAMES
        ]
        logger.info("Found %d KMS-related events in CloudTrail", len(kms_events))
        return kms_events

    except ClientError as e:
        logger.error("CloudTrail lookup error: %s", e)
        return []


def classify_event(event_name: str) -> str:
    """Classify a KMS event name into an action category."""
    name_lower = event_name.lower()
    if name_lower.startswith("encrypt") or name_lower.startswith("reencrypt"):
        return "encrypt"
    elif name_lower.startswith("decrypt"):
        return "decrypt"
    elif name_lower.startswith("sign"):
        return "sign"
    elif name_lower.startswith("verify"):
        return "verify"
    elif "generate" in name_lower and "data" in name_lower:
        return "generate_data_key"
    else:
        return "other"


def summarize_key_usage(
    key_id: str = "",
    hours_lookback: int = 24,
    region: str = "us-east-1",
) -> KeyUsageSummary:
    """
    Summarize key usage and crypto events from CloudTrail for a given key.

    Provider: AWS CloudTrail (boto3) - cloudtrail.us-east-1.amazonaws.com

    Args:
        key_id: The KMS key ID to summarize.
        hours_lookback: Number of hours to look back.
        region: AWS region.

    Returns:
        KeyUsageSummary with aggregated stats.
    """
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=hours_lookback)

    events_raw = lookup_kms_events(
        key_id=key_id,
        start_time=start_time,
        end_time=end_time,
        region=region,
    )

    summary = KeyUsageSummary(
        key_id=key_id or "all",
        period_start=start_time.timestamp(),
        period_end=end_time.timestamp(),
    )

    for evt in events_raw:
        event_name = evt.get("EventName", "Unknown")
        action = classify_event(event_name)
        event_time = evt.get("EventTime", datetime.now(timezone.utc))
        if isinstance(event_time, datetime):
            event_ts = event_time.timestamp()
        else:
            event_ts = 0.0

        cloudtrail_event = KeyUsageEvent(
            key_id=evt.get("Resources", [{}])[0].get("ResourceName", key_id) if evt.get("Resources") else key_id,
            action=action,
            timestamp=event_ts,
            status="SUCCESS",
            request_id=evt.get("EventId", ""),
        )
        summary.events.append(cloudtrail_event)
        summary.total_operations += 1

        if action == "encrypt":
            summary.encrypt_count += 1
        elif action == "decrypt":
            summary.decrypt_count += 1
        elif action == "sign":
            summary.sign_count += 1
        elif action == "verify":
            summary.verify_count += 1
        elif action == "generate_data_key":
            summary.generate_data_key_count += 1

    logger.info(
        "Key usage summary: %d total operations (%d encrypt, %d decrypt, "
        "%d sign, %d verify, %d generate_data_key)",
        summary.total_operations,
        summary.encrypt_count,
        summary.decrypt_count,
        summary.sign_count,
        summary.verify_count,
        summary.generate_data_key_count,
    )

    return summary


def format_summary_report(summary: KeyUsageSummary) -> str:
    """Format a KeyUsageSummary as a human-readable report."""
    lines = [
        f"=== Key Usage Summary ===",
        f"Key ID: {summary.key_id}",
        f"Period: {datetime.fromtimestamp(summary.period_start, tz=timezone.utc).isoformat()} "
        f"to {datetime.fromtimestamp(summary.period_end, tz=timezone.utc).isoformat()}",
        f"Total Operations: {summary.total_operations}",
        f"  - Encrypt: {summary.encrypt_count}",
        f"  - Decrypt: {summary.decrypt_count}",
        f"  - Sign: {summary.sign_count}",
        f"  - Verify: {summary.verify_count}",
        f"  - Generate Data Key: {summary.generate_data_key_count}",
        f"  - Errors: {summary.error_count}",
        f"=== End Report ===",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    sample_key_id = "arn:aws:kms:us-east-1:123456789012:key/sample-key-id"
    summary = summarize_key_usage(key_id=sample_key_id, hours_lookback=24)
    print(summary.to_json())
