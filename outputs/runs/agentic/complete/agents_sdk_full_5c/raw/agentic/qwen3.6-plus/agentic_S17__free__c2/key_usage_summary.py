"""
[LATER-STEP] key_usage_summary.py
Summarize key usage and crypto events using AWS KMS and AWS CloudTrail.
Provider: AWS Key Management Service (kms.amazonaws.com) and CloudTrail.
Retrieves key metadata, usage statistics, and recent CloudTrail events.
"""

import json
import sys
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from security_client import create_kms_client, KMSClientConfig, handle_kms_error

AWS_KMS_ENDPOINT = "kms.amazonaws.com"
AWS_CLOUDTRAIL_SERVICE = "cloudtrail"
AWS_KMS_SERVICE_NAME = "kms"

KMS_EVENT_NAMES = [
    "Encrypt",
    "Decrypt",
    "GenerateDataKey",
    "GenerateDataKeyWithoutPlaintext",
    "Sign",
    "Verify",
    "ReEncrypt",
    "DescribeKey",
    "ListKeys",
    "CreateGrant",
]


def get_key_metadata(
    key_id: str, config: Optional[KMSClientConfig] = None
) -> Dict[str, Any]:
    """
    Retrieve metadata for an AWS KMS key.
    """
    kms_client = create_kms_client(config)

    try:
        response = kms_client.describe_key(KeyId=key_id)
        key_metadata = response.get("KeyMetadata", {})
        return {
            "success": True,
            "key_id": key_metadata.get("KeyId"),
            "key_arn": key_metadata.get("Arn"),
            "key_state": key_metadata.get("KeyState"),
            "key_usage": key_metadata.get("KeyUsage"),
            "key_spec": key_metadata.get("KeySpec"),
            "creation_date": str(key_metadata.get("CreationDate", "")),
            "description": key_metadata.get("Description", ""),
            "origin": key_metadata.get("Origin"),
            "provider": "aws-kms",
            "endpoint": AWS_KMS_ENDPOINT,
        }
    except ClientError as e:
        error_result = handle_kms_error(e, "describe_key")
        return {"success": False, "error": error_result.get("error_message")}


def get_cloudtrail_key_events(
    key_id: str,
    hours_back: int = 24,
    max_events: int = 50,
    config: Optional[KMSClientConfig] = None,
) -> Dict[str, Any]:
    """
    Retrieve recent CloudTrail events for a KMS key.
    Uses AWS CloudTrail lookup_events API to find KMS operations.
    """
    if config is None:
        config = KMSClientConfig()

    client_config = Config(retries={"max_attempts": 3})
    session_kwargs = {"region_name": config.region}
    if config.aws_access_key_id and config.aws_secret_access_key:
        session_kwargs["aws_access_key_id"] = config.aws_access_key_id
        session_kwargs["aws_secret_access_key"] = config.aws_secret_access_key
    if config.aws_session_token:
        session_kwargs["aws_session_token"] = config.aws_session_token

    session = boto3.Session(**session_kwargs)
    cloudtrail_client = session.client(AWS_CLOUDTRAIL_SERVICE, config=client_config)

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours_back)

    events_summary = {}
    events_list = []

    try:
        for event_name in KMS_EVENT_NAMES:
            response = cloudtrail_client.lookup_events(
                LookupAttributes=[
                    {"AttributeKey": "ResourceName", "AttributeValue": key_id},
                    {"AttributeKey": "EventName", "AttributeValue": event_name},
                ],
                StartTime=start_time,
                EndTime=end_time,
                MaxResults=min(max_events, 50),
            )

            events = response.get("Events", [])
            event_count = len(events)

            if event_name not in events_summary:
                events_summary[event_name] = 0
            events_summary[event_name] += event_count

            for event in events:
                events_list.append(
                    {
                        "event_id": event.get("EventId"),
                        "event_name": event.get("EventName"),
                        "event_time": str(event.get("EventTime", "")),
                        "username": event.get("Username"),
                        "source": event.get("EventSource"),
                    }
                )

            if event_count > 0:
                break

        total_events = sum(events_summary.values())

        return {
            "success": True,
            "key_id": key_id,
            "time_window_hours": hours_back,
            "total_events": total_events,
            "events_by_type": events_summary,
            "recent_events": events_list[:max_events],
            "provider": "aws-cloudtrail",
            "endpoint": "cloudtrail.amazonaws.com",
        }

    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "Unknown")
        error_message = e.response.get("Error", {}).get("Message", str(e))
        return {
            "success": False,
            "error": f"CloudTrail error: {error_code} - {error_message}",
            "provider": "aws-cloudtrail",
        }


def generate_key_usage_summary(
    key_id: str,
    hours_back: int = 24,
    config: Optional[KMSClientConfig] = None,
) -> Dict[str, Any]:
    """
    Generate a comprehensive key usage summary combining KMS metadata
    and CloudTrail events for the specified KMS key.
    """
    metadata = get_key_metadata(key_id, config=config)

    if not metadata.get("success"):
        return metadata

    events = get_cloudtrail_key_events(
        key_id, hours_back=hours_back, config=config
    )

    summary = {
        "success": True,
        "key_metadata": metadata,
        "usage_statistics": events,
        "provider": "aws-kms",
        "endpoint": AWS_KMS_ENDPOINT,
        "report_generated_at": datetime.utcnow().isoformat(),
    }

    return summary


def key_usage_summary_to_json(
    key_id: str, hours_back: int = 24, config: Optional[KMSClientConfig] = None
) -> str:
    """Generate key usage summary and return as JSON string."""
    summary = generate_key_usage_summary(key_id, hours_back=hours_back, config=config)
    return json.dumps(summary, indent=2, default=str)


if __name__ == "__main__":
    key_id = "alias/my-encryption-key"

    summary = generate_key_usage_summary(
        key_id=key_id,
        hours_back=24,
    )

    print(json.dumps(summary, indent=2, default=str))
