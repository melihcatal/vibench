"""Summarize key usage and crypto events using AWS CloudTrail and KMS."""

import os
from typing import List, Dict, Optional

import boto3
from botocore.config import Config

from security_models import KeyUsageEvent, KeyUsageSummary


def get_cloudtrail_client(region: str = "us-east-1") -> boto3.client:
    """Create an AWS CloudTrail client."""
    creds = {
        "aws_access_key_id": os.environ.get("AWS_ACCESS_KEY_ID", ""),
        "aws_secret_access_key": os.environ.get("AWS_SECRET_ACCESS_KEY", ""),
    }
    config = Config(
        retries={"max_attempts": 3, "mode": "adaptive"},
        connect_timeout=5,
        read_timeout=30,
    )
    return boto3.client(
        "cloudtrail",
        region_name=region,
        aws_access_key_id=creds["aws_access_key_id"],
        aws_secret_access_key=creds["aws_secret_access_key"],
        config=config,
    )


def get_kms_client(region: str = "us-east-1") -> boto3.client:
    """Create an AWS KMS client."""
    creds = {
        "aws_access_key_id": os.environ.get("AWS_ACCESS_KEY_ID", ""),
        "aws_secret_access_key": os.environ.get("AWS_SECRET_ACCESS_KEY", ""),
    }
    config = Config(
        retries={"max_attempts": 3, "mode": "adaptive"},
        connect_timeout=5,
        read_timeout=30,
    )
    return boto3.client(
        "kms",
        region_name=region,
        aws_access_key_id=creds["aws_access_key_id"],
        aws_secret_access_key=creds["aws_secret_access_key"],
        config=config,
    )


KMS_EVENT_NAMES = {
    "Encrypt",
    "Decrypt",
    "GenerateDataKey",
    "GenerateDataKeyWithoutPlaintext",
    "ReEncrypt",
    "Sign",
    "Verify",
    "CreateGrant",
    "RetireGrant",
    "DescribeKey",
    "ListKeys",
    "DisableKey",
    "EnableKey",
    "ScheduleKeyDeletion",
    "CreateKey",
    "UpdateKeyDescription",
    "GenerateRandom",
}


def fetch_key_usage_events(
    key_id: str,
    max_events: int = 100,
    region: str = "us-east-1",
) -> List[KeyUsageEvent]:
    """Fetch recent KMS usage events from AWS CloudTrail.

    CloudTrail records API calls made to AWS KMS. This queries those
    events for a specific KMS key ID.

    Args:
        key_id: The AWS KMS key ID to look up events for.
        max_events: Maximum number of events to return.
        region: AWS region for CloudTrail lookup.

    Returns:
        List of KeyUsageEvent objects.
    """
    ct = get_cloudtrail_client(region=region)
    events = []

    try:
        response = ct.lookup_events(
            LookupAttributes=[
                {"AttributeKey": "ResourceName", "AttributeValue": key_id},
                {"AttributeKey": "EventCategory", "AttributeValue": "insight"},
            ],
            MaxResults=min(max_events, 50),
        )
    except Exception:
        response = ct.lookup_events(
            LookupAttributes=[
                {"AttributeKey": "ResourceName", "AttributeValue": key_id},
            ],
            MaxResults=min(max_events, 50),
        )

    for event in response.get("Events", []):
        event_name = event.get("EventName", "")
        if event_name not in KMS_EVENT_NAMES:
            continue

        cloud_trail_event = event.get("CloudTrailEvent", "{}")
        import json
        try:
            ct_data = json.loads(cloud_trail_event)
        except (json.JSONDecodeError, TypeError):
            ct_data = {}

        user_identity = ct_data.get("userIdentity", {}).get("arn", "unknown")
        source_ip = ct_data.get("sourceIPAddress", "unknown")
        aws_region = ct_data.get("awsRegion", region)
        timestamp = event.get("EventTime", "")

        events.append(KeyUsageEvent(
            timestamp=str(timestamp),
            event_name=event_name,
            key_id=key_id,
            user_identity=user_identity,
            source_ip=source_ip,
            region=aws_region,
        ))

    return events


def summarize_key_usage(
    key_id: str,
    events: Optional[List[KeyUsageEvent]] = None,
    region: str = "us-east-1",
) -> KeyUsageSummary:
    """Generate a summary of key usage for a given KMS key.

    Counts operations by type from CloudTrail events.

    Args:
        key_id: AWS KMS key ID.
        events: Optional pre-fetched events. If None, events are fetched.
        region: AWS region.

    Returns:
        KeyUsageSummary with operation counts.
    """
    if events is None:
        events = fetch_key_usage_events(key_id, region=region)

    encrypt_count = 0
    decrypt_count = 0
    sign_count = 0
    verify_count = 0
    generate_data_key_count = 0

    for event in events:
        name = event.event_name
        if name in ("Encrypt", "ReEncrypt"):
            encrypt_count += 1
        elif name == "Decrypt":
            decrypt_count += 1
        elif name == "Sign":
            sign_count += 1
        elif name == "Verify":
            verify_count += 1
        elif name.startswith("GenerateDataKey"):
            generate_data_key_count += 1

    total = len(events)
    return KeyUsageSummary(
        key_id=key_id,
        total_operations=total,
        encrypt_count=encrypt_count,
        decrypt_count=decrypt_count,
        sign_count=sign_count,
        verify_count=verify_count,
        generate_data_key_count=generate_data_key_count,
        recent_events=events[:10],
    )


if __name__ == "__main__":
    import json

    key_id = os.environ.get("AWS_KMS_KEY_ID", "")
    if key_id:
        summary = summarize_key_usage(key_id)
        print(f"Key ID: {summary.key_id}")
        print(f"Total operations: {summary.total_operations}")
        print(f"Encrypt: {summary.encrypt_count}")
        print(f"Decrypt: {summary.decrypt_count}")
        print(f"Sign: {summary.sign_count}")
        print(f"Verify: {summary.verify_count}")
        print(f"GenerateDataKey: {summary.generate_data_key_count}")
