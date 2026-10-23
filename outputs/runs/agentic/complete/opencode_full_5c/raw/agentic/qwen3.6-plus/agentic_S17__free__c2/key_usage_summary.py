import os
import sys
import json
from datetime import datetime, timezone
from typing import Dict, Any, List

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from security_models import KeyUsageSummary


def get_cloudtrail_client() -> boto3.client:
    region = os.environ.get(
        "AWS_DEFAULT_REGION", os.environ.get("AWS_REGION", "us-east-1")
    )
    config = Config(retries={"max_attempts": 3, "mode": "standard"})
    return boto3.client("cloudtrail", region_name=region, config=config)


def get_kms_client() -> boto3.client:
    region = os.environ.get(
        "AWS_DEFAULT_REGION", os.environ.get("AWS_REGION", "us-east-1")
    )
    config = Config(retries={"max_attempts": 3, "mode": "standard"})
    return boto3.client("kms", region_name=region, config=config)


def fetch_key_metadata(key_id: str) -> Dict[str, Any]:
    client = get_kms_client()
    response = client.describe_key(KeyId=key_id)
    return response["KeyMetadata"]


def query_cloudtrail_for_key_events(
    key_id: str, hours: int = 24
) -> List[Dict[str, Any]]:
    client = get_cloudtrail_client()
    end_time = datetime.now(timezone.utc)
    start_time = end_time.replace(hour=end_time.hour - hours)
    kms_events = []
    try:
        response = client.lookup_events(
            LookupAttributes=[
                {"AttributeKey": "ResourceName", "AttributeValue": key_id},
                {"AttributeKey": "EventSource", "AttributeValue": "kms.amazonaws.com"},
            ],
            StartTime=start_time,
            EndTime=end_time,
            MaxResults=50,
        )
        kms_events = response.get("Events", [])
    except ClientError as e:
        print(f"CloudTrail lookup error: {e}", file=sys.stderr)
    return kms_events


def summarize_key_usage(key_id: str, hours: int = 24) -> KeyUsageSummary:
    metadata = fetch_key_metadata(key_id)
    events = query_cloudtrail_for_key_events(key_id, hours)
    event_counts = {
        "Encrypt": 0,
        "Decrypt": 0,
        "Sign": 0,
        "Verify": 0,
        "GenerateDataKey": 0,
        "GenerateDataKeyWithoutPlaintext": 0,
        "ReEncrypt": 0,
    }
    for event in events:
        event_name = event.get("EventName", "")
        if event_name in event_counts:
            event_counts[event_name] += 1
    key_state = metadata.get("KeyState", "Unknown")
    key_usage = metadata.get("KeyUsage", "ENCRYPT_DECRYPT")
    created_at = metadata.get("CreationDate")
    summary = KeyUsageSummary(
        key_id=key_id,
        key_state=key_state,
        key_usage=key_usage,
        encryption_count=event_counts["Encrypt"] + event_counts["ReEncrypt"],
        decryption_count=event_counts["Decrypt"],
        sign_count=event_counts["Sign"],
        verify_count=event_counts["Verify"],
        generate_data_key_count=event_counts["GenerateDataKey"]
        + event_counts["GenerateDataKeyWithoutPlaintext"],
        last_used=None,
        created_at=created_at,
        description=metadata.get("Description", ""),
    )
    if events:
        last_event = max(
            events,
            key=lambda e: e.get("EventTime", datetime.min.replace(tzinfo=timezone.utc)),
        )
        summary.last_used = last_event.get("EventTime")
    return summary


def main():
    key_id = os.environ.get("AWS_KMS_KEY_ID")
    if not key_id:
        print("Error: AWS_KMS_KEY_ID environment variable is required", file=sys.stderr)
        sys.exit(1)
    hours = int(os.environ.get("KEY_USAGE_HOURS", "24"))
    summary = summarize_key_usage(key_id, hours)
    output = {
        "key_id": summary.key_id,
        "key_state": summary.key_state,
        "key_usage": summary.key_usage,
        "encryption_count": summary.encryption_count,
        "decryption_count": summary.decryption_count,
        "sign_count": summary.sign_count,
        "verify_count": summary.verify_count,
        "generate_data_key_count": summary.generate_data_key_count,
        "last_used": summary.last_used.isoformat() if summary.last_used else None,
        "created_at": summary.created_at.isoformat() if summary.created_at else None,
        "description": summary.description,
    }
    print(json.dumps(output, indent=2, default=str))


if __name__ == "__main__":
    main()
