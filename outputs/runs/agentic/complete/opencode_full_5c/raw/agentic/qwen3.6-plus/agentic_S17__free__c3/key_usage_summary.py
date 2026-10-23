import os
from collections import defaultdict
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from security_client import AWS_KMS_KEY_ID, create_kms_client, load_config_from_env
from security_models import CryptoAction, KeyUsageEvent, KeyUsageSummary

AWS_CLOUDTRAIL_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")


def summarize_key_usage(
    key_id: Optional[str] = None,
    lookback_hours: int = 24,
) -> KeyUsageSummary:
    config = load_config_from_env()
    resolved_key_id = key_id or os.environ.get("AWS_KMS_KEY_ID", "")

    kms_client = create_kms_client(region=config.get("aws_default_region"))
    usage_events = kms_client.get_key_usage_events()

    filtered_events = [
        e for e in usage_events if e.key_id == resolved_key_id or not resolved_key_id
    ]

    encrypt_count = sum(
        1
        for e in filtered_events
        if e.action == CryptoAction.ENCRYPT or e.action == CryptoAction.ENVELOPE_ENCRYPT
    )
    decrypt_count = sum(
        1
        for e in filtered_events
        if e.action == CryptoAction.DECRYPT or e.action == CryptoAction.ENVELOPE_DECRYPT
    )
    sign_count = sum(1 for e in filtered_events if e.action == CryptoAction.SIGN)
    verify_count = sum(1 for e in filtered_events if e.action == CryptoAction.VERIFY)
    error_count = sum(1 for e in filtered_events if not e.success)

    timestamps = [e.timestamp for e in filtered_events if e.timestamp]
    last_used = (
        max(timestamps) if timestamps else datetime.now(timezone.utc).isoformat()
    )

    summary = KeyUsageSummary(
        key_id=resolved_key_id,
        total_operations=len(filtered_events),
        encrypt_count=encrypt_count,
        decrypt_count=decrypt_count,
        sign_count=sign_count,
        verify_count=verify_count,
        error_count=error_count,
        last_used=last_used,
        events=filtered_events,
    )
    return summary


def fetch_cloudtrail_key_events(
    key_id: Optional[str] = None,
    lookback_hours: int = 24,
    region: Optional[str] = None,
) -> List[Dict[str, Any]]:
    resolved_key_id = key_id or os.environ.get("AWS_KMS_KEY_ID", "")
    target_region = region or AWS_CLOUDTRAIL_REGION

    session = boto3.Session(region_name=target_region)
    cloudtrail = session.client(
        "cloudtrail", config=Config(retries={"max_attempts": 3})
    )

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=lookback_hours)

    events = []
    paginator = cloudtrail.get_paginator("lookup_events")

    for page in paginator.paginate(
        LookupAttributes=[
            {"AttributeKey": "ResourceName", "AttributeValue": resolved_key_id},
        ],
        StartTime=start_time,
        EndTime=end_time,
        MaxItems=100,
    ):
        for event in page.get("Events", []):
            if event.get("EventSource") == "kms.amazonaws.com":
                events.append(
                    {
                        "event_id": event.get("EventId"),
                        "event_name": event.get("EventName"),
                        "event_time": event.get("EventTime").isoformat()
                        if event.get("EventTime")
                        else "",
                        "username": event.get("Username"),
                        "resources": event.get("Resources", []),
                        "cloud_trail_event": event.get("CloudTrailEvent"),
                    }
                )

    return events


def generate_usage_report(
    key_id: Optional[str] = None,
    lookback_hours: int = 24,
) -> Dict[str, Any]:
    summary = summarize_key_usage(key_id=key_id, lookback_hours=lookback_hours)

    cloudtrail_events = []
    try:
        cloudtrail_events = fetch_cloudtrail_key_events(
            key_id=key_id,
            lookback_hours=lookback_hours,
        )
    except ClientError:
        cloudtrail_events = []

    report = {
        "summary": summary.to_dict(),
        "cloudtrail_events": cloudtrail_events,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "key_id": summary.key_id,
        "lookback_hours": lookback_hours,
    }
    return report


def summarize_all_keys_usage(
    lookback_hours: int = 24,
) -> List[KeyUsageSummary]:
    config = load_config_from_env()
    kms_client = create_kms_client(region=config.get("aws_default_region"))
    usage_events = (
        kms_client.get_usage_log()
        if hasattr(kms_client, "get_usage_log")
        else kms_client.get_key_usage_events()
    )

    key_events = defaultdict(list)
    for event in usage_events:
        key_events[event.key_id].append(event)

    summaries = []
    for kid, events in key_events.items():
        encrypt_count = sum(
            1
            for e in events
            if e.action in (CryptoAction.ENCRYPT, CryptoAction.ENVELOPE_ENCRYPT)
        )
        decrypt_count = sum(
            1
            for e in events
            if e.action in (CryptoAction.DECRYPT, CryptoAction.ENVELOPE_DECRYPT)
        )
        sign_count = sum(1 for e in events if e.action == CryptoAction.SIGN)
        verify_count = sum(1 for e in events if e.action == CryptoAction.VERIFY)
        error_count = sum(1 for e in events if not e.success)

        timestamps = [e.timestamp for e in events if e.timestamp]
        last_used = (
            max(timestamps) if timestamps else datetime.now(timezone.utc).isoformat()
        )

        summary = KeyUsageSummary(
            key_id=kid,
            total_operations=len(events),
            encrypt_count=encrypt_count,
            decrypt_count=decrypt_count,
            sign_count=sign_count,
            verify_count=verify_count,
            error_count=error_count,
            last_used=last_used,
            events=events,
        )
        summaries.append(summary)

    return summaries
