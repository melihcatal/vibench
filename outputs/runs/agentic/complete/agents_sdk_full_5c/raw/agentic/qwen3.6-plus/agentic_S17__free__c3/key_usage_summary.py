"""
Summarize key usage and crypto events using AWS CloudTrail.

Uses the AWS CloudTrail API (cloudtrail.amazonaws.com) with the boto3 SDK
to query and summarize KMS key usage events from CloudTrail logs,
including encryption, decryption, signing, and verification operations.
"""

import os
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta

from security_client import get_cloudtrail_client
from security_models import (
    KeyUsageSummary,
    KeyUsageEvent,
    build_key_usage_from_events,
    normalize_key_id,
)

logger = logging.getLogger(__name__)


def get_key_usage_events(
    key_id: str,
    hours_back: int = 24,
    max_events: int = 1000,
    region: Optional[str] = None,
    client=None,
) -> List[Dict[str, Any]]:
    """
    Retrieve KMS key usage events from AWS CloudTrail.

    Provider: AWS CloudTrail (cloudtrail.amazonaws.com)
    API: cloudtrail.lookup_events

    Args:
        key_id: AWS KMS key ID or ARN to look up events for.
        hours_back: Number of hours to look back (default: 24).
        max_events: Maximum number of events to retrieve.
        region: Optional AWS region override.
        client: Optional pre-initialized CloudTrail client.

    Returns:
        List of CloudTrail event dictionaries.
    """
    if client is None:
        client = get_cloudtrail_client(region=region)

    normalized_key = normalize_key_id(key_id)

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours_back)

    lookup_attributes = [
        {
            "AttributeKey": "ResourceName",
            "AttributeValue": normalized_key,
        }
    ]

    kms_event_names = [
        "Encrypt",
        "Decrypt",
        "GenerateDataKey",
        "GenerateDataKeyWithoutPlaintext",
        "Sign",
        "Verify",
        "ReEncrypt",
        "GenerateRandom",
    ]

    all_events = []
    next_token = None

    for event_name in kms_event_names:
        params = {
            "LookupAttributes": lookup_attributes,
            "StartTime": start_time,
            "EndTime": end_time,
            "MaxResults": min(max_events, 100),
        }

        if next_token:
            params["NextToken"] = next_token

        try:
            response = client.lookup_events(**params)
            events = response.get("Events", [])

            for event in events:
                event_data = event.get("CloudTrailEvent", "")
                event["eventName"] = event.get("EventName", "")
                event["eventTime"] = event.get("EventTime", "").isoformat()
                all_events.append(event)

        except Exception as e:
            logger.warning(
                "Failed to lookup CloudTrail events for %s (%s): %s",
                event_name,
                normalized_key,
                str(e),
            )
            continue

    logger.info(
        "Retrieved %d CloudTrail events for AWS KMS key %s",
        len(all_events),
        normalized_key,
    )

    return all_events[:max_events]


def summarize_key_usage(
    key_id: str,
    hours_back: int = 24,
    max_events: int = 1000,
    region: Optional[str] = None,
    events_override: Optional[List[Dict[str, Any]]] = None,
) -> KeyUsageSummary:
    """
    Generate a KeyUsageSummary for a given KMS key.

    Provider: AWS CloudTrail (cloudtrail.amazonaws.com)
    API: cloudtrail.lookup_events (via get_key_usage_events)

    Args:
        key_id: AWS KMS key ID or ARN.
        hours_back: Number of hours to look back for events.
        max_events: Maximum events to include.
        region: Optional AWS region override.
        events_override: Optional pre-fetched events list (skips CloudTrail lookup).

    Returns:
        KeyUsageSummary with aggregated statistics.
    """
    if events_override is not None:
        events = events_override
    else:
        events = get_key_usage_events(
            key_id=key_id,
            hours_back=hours_back,
            max_events=max_events,
            region=region,
        )

    summary = build_key_usage_from_events(key_id, events)
    summary.key_id = normalize_key_id(key_id)

    logger.info(
        "Key usage summary for %s: %d total ops (encrypt: %d, decrypt: %d, "
        "sign: %d, verify: %d), %d unique users",
        summary.key_id,
        summary.total_operations,
        summary.encrypt_count,
        summary.decrypt_count,
        summary.sign_count,
        summary.verify_count,
        summary.unique_users,
    )

    return summary


def get_usage_report_json(
    key_id: str,
    hours_back: int = 24,
) -> str:
    """
    Generate a JSON-formatted usage report for a KMS key.

    Args:
        key_id: AWS KMS key ID or ARN.
        hours_back: Number of hours to look back.

    Returns:
        JSON string with usage summary and recent events.
    """
    import json

    summary = summarize_key_usage(key_id, hours_back=hours_back)

    report = {
        "key_id": summary.key_id,
        "provider": "aws_kms",
        "cloudtrail_endpoint": "cloudtrail.amazonaws.com",
        "summary": {
            "total_operations": summary.total_operations,
            "encrypt_count": summary.encrypt_count,
            "decrypt_count": summary.decrypt_count,
            "sign_count": summary.sign_count,
            "verify_count": summary.verify_count,
            "unique_users": summary.unique_users,
        },
        "recent_events": [
            {
                "timestamp": evt.timestamp,
                "event_name": evt.event_name,
                "user_identity": evt.user_identity,
                "source_ip": evt.source_ip,
                "region": evt.region,
                "result": evt.result,
            }
            for evt in summary.event_log[:50]
        ],
    }

    return json.dumps(report, indent=2)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sample_key = os.environ.get("AWS_KMS_DEFAULT_KEY_ID", "")
    if sample_key:
        report = get_usage_report_json(sample_key, hours_back=24)
        print(report)
    else:
        print("Set AWS_KMS_DEFAULT_KEY_ID environment variable to test.")
