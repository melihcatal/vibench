"""
key_usage_summary.py - Summarizes key usage and crypto events from AWS CloudTrail.

Queries AWS CloudTrail lookup_events API for KMS-related events (Encrypt, Decrypt,
GenerateDataKey, Sign, Verify, etc.) and aggregates usage statistics per key.
Includes event timeline and operation counts.

Provider: AWS CloudTrail (boto3 client for cloudtrail.us-east-1.amazonaws.com)
Service: kms.amazonaws.com via CloudTrail event lookup
"""

import json
import logging
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import boto3
from botocore.config import Config

from security_models import KeyUsageSummary

logger = logging.getLogger(__name__)

KMS_SERVICE_NAME = "kms.amazonaws.com"

KMS_OPERATIONS = {
    "Encrypt",
    "Decrypt",
    "GenerateDataKey",
    "GenerateDataKeyWithoutPlaintext",
    "Sign",
    "Verify",
    "ReEncryptTo",
    "ReEncryptFrom",
    "CreateGrant",
    "RetireGrant",
    "DisableKey",
    "EnableKey",
    "ScheduleKeyDeletion",
    "CancelKeyDeletion",
    "DescribeKey",
    "ListKeys",
    "ListAliases",
    "CreateKey",
    "UpdateKeyDescription",
    "RotateKeyOnDemand",
}

REGION = "us-east-1"


def get_cloudtrail_client(region: str = REGION) -> boto3.client:
    """
    Initialize an AWS CloudTrail client via boto3.
    CloudTrail endpoint: cloudtrail.us-east-1.amazonaws.com
    """
    config = Config(
        retries={"max_attempts": 3, "mode": "adaptive"},
        region_name=region,
    )
    return boto3.client("cloudtrail", config=config)


def lookup_kms_events(
    key_id: str,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    region: str = REGION,
    max_results: int = 100,
) -> List[Dict[str, Any]]:
    """
    Look up KMS events for a specific key ID from AWS CloudTrail.

    Args:
        key_id: The KMS key ID to filter events for.
        start_time: Start of the time window. Defaults to 7 days ago.
        end_time: End of the time window. Defaults to now.
        region: AWS region for CloudTrail.
        max_results: Maximum events to retrieve.

    Returns:
        List of CloudTrail event dicts.
    """
    client = get_cloudtrail_client(region)

    if start_time is None:
        start_time = datetime.utcnow() - timedelta(days=7)
    if end_time is None:
        end_time = datetime.utcnow()

    events = []
    paginator = client.get_paginator("lookup_events")

    page_iterator = paginator.paginate(
        LookupAttributes=[
            {"AttributeKey": "ResourceName", "AttributeValue": key_id},
            {"AttributeKey": "ReadOnly", "AttributeValue": "false"},
        ],
        StartTime=start_time,
        EndTime=end_time,
        PaginationConfig={"MaxItems": max_results, "PageSize": 50},
    )

    for page in page_iterator:
        for event in page.get("Events", []):
            if event.get("EventSource") == KMS_SERVICE_NAME:
                events.append(event)

    logger.info("Found %d KMS events for key %s in CloudTrail", len(events), key_id)
    return events


def summarize_key_usage(
    key_id: str,
    events: Optional[List[Dict[str, Any]]] = None,
    region: str = REGION,
) -> KeyUsageSummary:
    """
    Summarize KMS key usage from CloudTrail events.

    Counts operations by type (Encrypt, Decrypt, Sign, etc.) and provides
    a structured KeyUsageSummary with date range and event details.

    Args:
        key_id: The KMS key ID.
        events: Pre-fetched events list. If None, fetches from CloudTrail.
        region: AWS region.

    Returns:
        KeyUsageSummary with aggregated statistics.
    """
    if events is None:
        events = lookup_kms_events(key_id, region=region)

    operation_counts: Dict[str, int] = defaultdict(int)
    event_details: List[Dict[str, Any]] = []
    timestamps: List[str] = []

    for event in events:
        event_name = event.get("EventName", "Unknown")
        operation_counts[event_name] += 1
        timestamps.append(event.get("EventTime", "").isoformat())

        event_details.append({
            "event_name": event_name,
            "event_time": event.get("EventTime", "").isoformat(),
            "username": event.get("Username", ""),
            "source_ip": event.get("SourceIPAddress", ""),
            "event_id": event.get("EventId", ""),
        })

    encryption_count = operation_counts.get("Encrypt", 0) + operation_counts.get("ReEncryptTo", 0) + operation_counts.get("ReEncryptFrom", 0)
    decryption_count = operation_counts.get("Decrypt", 0)
    signing_count = operation_counts.get("Sign", 0) + operation_counts.get("GenerateDataKey", 0)
    verification_count = operation_counts.get("Verify", 0)
    total_ops = sum(operation_counts.values())

    date_range = {}
    if timestamps:
        sorted_ts = sorted(timestamps)
        date_range = {
            "start": sorted_ts[0],
            "end": sorted_ts[-1],
        }

    summary = KeyUsageSummary(
        key_id=key_id,
        total_operations=total_ops,
        encryption_count=encryption_count,
        decryption_count=decryption_count,
        signing_count=signing_count,
        verification_count=verification_count,
        date_range=date_range,
        events=event_details,
    )

    logger.info(
        "Key usage summary for %s: %d total operations",
        key_id,
        total_ops,
    )
    return summary


def main():
    """CLI entry point for key_usage_summary."""
    if len(sys.argv) < 2:
        print("Usage: python key_usage_summary.py <key_id> [region] [max_results]")
        sys.exit(1)

    key_id = sys.argv[1]
    region = sys.argv[2] if len(sys.argv) > 2 else REGION
    max_results = int(sys.argv[3]) if len(sys.argv) > 3 else 100

    logging.basicConfig(level=logging.INFO)
    summary = summarize_key_usage(key_id, region=region)

    output = {
        "key_id": summary.key_id,
        "total_operations": summary.total_operations,
        "encryption_count": summary.encryption_count,
        "decryption_count": summary.decryption_count,
        "signing_count": summary.signing_count,
        "verification_count": summary.verification_count,
        "date_range": summary.date_range,
        "events": summary.events[:20],
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
