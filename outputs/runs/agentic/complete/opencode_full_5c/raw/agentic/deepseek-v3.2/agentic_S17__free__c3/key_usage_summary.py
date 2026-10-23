import os
import json
from datetime import datetime, timedelta
import boto3
from botocore.exceptions import ClientError
from typing import Dict, List, Any, Optional


def get_key_usage_summary(key_id=None, days=30):
    """
    Summarize key usage and crypto events from AWS CloudTrail.

    Args:
        key_id: AWS KMS key ID or alias
        days: Number of days to look back

    Returns:
        dict with key usage summary
    """
    if key_id is None:
        key_id = os.environ.get("AWS_KMS_KEY_ID", "alias/encryption-key")

    cloudtrail_client = boto3.client(
        "cloudtrail", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )
    kms_client = boto3.client(
        "kms", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=days)

    try:
        lookup_events_response = cloudtrail_client.lookup_events(
            LookupAttributes=[
                {"AttributeKey": "ResourceName", "AttributeValue": key_id}
            ],
            StartTime=start_time,
            EndTime=end_time,
            MaxResults=100,
        )

        events = lookup_events_response.get("Events", [])

        event_counts = {}
        for event in events:
            event_name = event.get("EventName", "Unknown")
            event_counts[event_name] = event_counts.get(event_name, 0) + 1

        key_metadata = kms_client.describe_key(KeyId=key_id)

        key_rotation_response = kms_client.get_key_rotation_status(KeyId=key_id)

        return {
            "key_id": key_id,
            "key_arn": key_metadata["KeyMetadata"]["Arn"],
            "key_state": key_metadata["KeyMetadata"]["KeyState"],
            "key_usage": key_metadata["KeyMetadata"]["KeyUsage"],
            "rotation_enabled": key_rotation_response.get("KeyRotationEnabled", False),
            "analysis_period_days": days,
            "total_events": len(events),
            "event_counts": event_counts,
            "top_events": sorted(
                event_counts.items(), key=lambda x: x[1], reverse=True
            )[:5],
            "last_event_time": events[0].get("EventTime").isoformat()
            if events
            else None,
            "provider": "aws_kms",
            "generated_at": datetime.utcnow().isoformat(),
        }
    except ClientError as e:
        raise Exception(f"Failed to get key usage summary: {e}")


def get_crypto_operations_summary(key_ids=None, days=7):
    """
    Get summary of cryptographic operations for multiple keys.

    Args:
        key_ids: List of key IDs or aliases
        days: Number of days to look back

    Returns:
        dict with crypto operations summary
    """
    if key_ids is None:
        key_ids = [os.environ.get("AWS_KMS_KEY_ID", "alias/encryption-key")]

    cloudtrail_client = boto3.client(
        "cloudtrail", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=days)

    crypto_operations = [
        "Encrypt",
        "Decrypt",
        "GenerateDataKey",
        "Sign",
        "Verify",
        "ReEncrypt",
        "GenerateDataKeyWithoutPlaintext",
    ]

    summary = {
        "period_days": days,
        "keys": [],
        "total_operations": 0,
        "operations_by_type": {},
        "provider": "aws_kms",
        "generated_at": datetime.utcnow().isoformat(),
    }

    for key_id in key_ids:
        try:
            lookup_events_response = cloudtrail_client.lookup_events(
                LookupAttributes=[
                    {"AttributeKey": "ResourceName", "AttributeValue": key_id}
                ],
                StartTime=start_time,
                EndTime=end_time,
                MaxResults=50,
            )

            events = lookup_events_response.get("Events", [])
            key_ops = {}

            for event in events:
                event_name = event.get("EventName", "Unknown")
                if event_name in crypto_operations:
                    key_ops[event_name] = key_ops.get(event_name, 0) + 1
                    summary["operations_by_type"][event_name] = (
                        summary["operations_by_type"].get(event_name, 0) + 1
                    )

            key_summary = {
                "key_id": key_id,
                "total_operations": sum(key_ops.values()),
                "operations": key_ops,
                "event_count": len(events),
            }

            summary["keys"].append(key_summary)
            summary["total_operations"] += key_summary["total_operations"]

        except ClientError as e:
            print(f"Warning: Could not get events for key {key_id}: {e}")

    return summary


def generate_key_usage_report(key_id=None, output_format="json"):
    """
    Generate a comprehensive key usage report.

    Args:
        key_id: AWS KMS key ID or alias
        output_format: Output format ('json' or 'text')

    Returns:
        Report in specified format
    """
    if key_id is None:
        key_id = os.environ.get("AWS_KMS_KEY_ID", "alias/encryption-key")

    kms_client = boto3.client(
        "kms", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    try:
        key_metadata = kms_client.describe_key(KeyId=key_id)
        key_rotation = kms_client.get_key_rotation_status(KeyId=key_id)

        usage_summary = get_key_usage_summary(key_id, days=30)
        ops_summary = get_crypto_operations_summary([key_id], days=7)

        report = {
            "key_info": {
                "key_id": key_metadata["KeyMetadata"]["KeyId"],
                "arn": key_metadata["KeyMetadata"]["Arn"],
                "description": key_metadata["KeyMetadata"].get("Description", ""),
                "creation_date": key_metadata["KeyMetadata"][
                    "CreationDate"
                ].isoformat(),
                "key_state": key_metadata["KeyMetadata"]["KeyState"],
                "key_usage": key_metadata["KeyMetadata"]["KeyUsage"],
                "key_spec": key_metadata["KeyMetadata"]["KeySpec"],
                "origin": key_metadata["KeyMetadata"]["Origin"],
            },
            "rotation_info": {
                "rotation_enabled": key_rotation.get("KeyRotationEnabled", False),
                "rotation_period_days": key_rotation.get("RotationPeriodInDays", 365),
            },
            "usage_summary_30d": usage_summary,
            "operations_summary_7d": ops_summary,
            "report_generated": datetime.utcnow().isoformat(),
            "provider": "aws_kms",
        }

        if output_format == "json":
            return json.dumps(report, indent=2, default=str)
        else:
            lines = [
                f"Key Usage Report for {key_id}",
                f"Generated: {datetime.utcnow().isoformat()}",
                "",
                f"Key ID: {key_metadata['KeyMetadata']['KeyId']}",
                f"State: {key_metadata['KeyMetadata']['KeyState']}",
                f"Usage: {key_metadata['KeyMetadata']['KeyUsage']}",
                f"Rotation Enabled: {key_rotation.get('KeyRotationEnabled', False)}",
                "",
                f"Total Events (30 days): {usage_summary.get('total_events', 0)}",
                "Top Events:",
            ]

            for event, count in usage_summary.get("top_events", []):
                lines.append(f"  {event}: {count}")

            lines.extend(
                [
                    "",
                    f"Crypto Operations (7 days): {ops_summary.get('total_operations', 0)}",
                    "Operations by Type:",
                ]
            )

            for op_type, count in ops_summary.get("operations_by_type", {}).items():
                lines.append(f"  {op_type}: {count}")

            return "\n".join(lines)

    except ClientError as e:
        raise Exception(f"Failed to generate key usage report: {e}")


if __name__ == "__main__":
    summary = get_key_usage_summary()
    print(f"Key usage summary: {json.dumps(summary, indent=2, default=str)}")
