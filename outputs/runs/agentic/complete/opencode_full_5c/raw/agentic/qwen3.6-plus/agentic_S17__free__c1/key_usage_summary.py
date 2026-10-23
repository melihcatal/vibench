import os
import json
from datetime import datetime, timedelta
from typing import Optional, List
import boto3
from security_models import KeyUsageSummary, KeyUsageEvent
from security_client import get_cloudtrail_client, load_aws_config


def summarize_key_usage(
    key_id: str = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    max_events: int = 100,
) -> KeyUsageSummary:
    config = load_aws_config()
    cloudtrail_client = get_cloudtrail_client(config)

    target_key_id = key_id or os.environ.get("AWS_KMS_KEY_ID", "")

    if start_time is None:
        start_time = datetime.utcnow() - timedelta(hours=24)
    if end_time is None:
        end_time = datetime.utcnow()

    lookup_attributes = [
        {"AttributeKey": "ResourceName", "AttributeValue": target_key_id},
    ]

    kms_event_names = [
        "Encrypt",
        "Decrypt",
        "GenerateDataKey",
        "GenerateDataKeyWithoutPlaintext",
        "Sign",
        "Verify",
        "CreateGrant",
        "RetireGrant",
    ]

    events = []
    encrypt_count = 0
    decrypt_count = 0
    generate_data_key_count = 0
    sign_count = 0
    verify_count = 0

    response = cloudtrail_client.lookup_events(
        LookupAttributes=lookup_attributes,
        StartTime=start_time,
        EndTime=end_time,
        MaxResults=50,
    )

    for event in response.get("Events", [])[:max_events]:
        event_name = event.get("EventName", "")
        if event_name not in kms_event_names:
            continue

        cloud_trail_event = event.get("CloudTrailEvent", "{}")
        try:
            event_details = json.loads(cloud_trail_event)
        except (json.JSONDecodeError, TypeError):
            event_details = {}

        user_identity = event.get("Username", "unknown")
        source_ip = event.get("AccessKeyId", "unknown")
        event_time = (
            event.get("EventTime", "").isoformat()
            if hasattr(event.get("EventTime", ""), "isoformat")
            else str(event.get("EventTime", ""))
        )

        encryption_context = event_details.get("requestParameters", {}).get(
            "encryptionContext", {}
        )

        usage_event = KeyUsageEvent(
            key_id=target_key_id,
            event_name=event_name,
            event_time=event_time,
            user_identity=user_identity,
            source_ip=source_ip,
            encryption_context=encryption_context,
        )
        events.append(usage_event)

        if event_name == "Encrypt":
            encrypt_count += 1
        elif event_name == "Decrypt":
            decrypt_count += 1
        elif event_name in ("GenerateDataKey", "GenerateDataKeyWithoutPlaintext"):
            generate_data_key_count += 1
        elif event_name == "Sign":
            sign_count += 1
        elif event_name == "Verify":
            verify_count += 1

    total_operations = (
        encrypt_count
        + decrypt_count
        + generate_data_key_count
        + sign_count
        + verify_count
    )

    return KeyUsageSummary(
        key_id=target_key_id,
        total_operations=total_operations,
        encrypt_count=encrypt_count,
        decrypt_count=decrypt_count,
        generate_data_key_count=generate_data_key_count,
        sign_count=sign_count,
        verify_count=verify_count,
        events=events,
    )


def format_key_usage_report(summary: KeyUsageSummary) -> str:
    lines = [
        f"AWS KMS Key Usage Summary",
        f"Key ID: {summary.key_id}",
        f"Total Operations: {summary.total_operations}",
        f"  Encrypt: {summary.encrypt_count}",
        f"  Decrypt: {summary.decrypt_count}",
        f"  GenerateDataKey: {summary.generate_data_key_count}",
        f"  Sign: {summary.sign_count}",
        f"  Verify: {summary.verify_count}",
        f"Events ({len(summary.events)}):",
    ]
    for event in summary.events[:10]:
        lines.append(
            f"  - {event.event_name} at {event.event_time} by {event.user_identity}"
        )
    return "\n".join(lines)


if __name__ == "__main__":
    summary = summarize_key_usage()
    print(format_key_usage_report(summary))
