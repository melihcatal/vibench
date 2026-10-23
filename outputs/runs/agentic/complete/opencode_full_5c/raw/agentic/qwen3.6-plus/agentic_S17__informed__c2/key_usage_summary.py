import os
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, List

from security_client import (
    get_kms_client,
    get_cloudwatch_logs_client,
    resolve_key_id,
    parse_kms_error,
)
from security_models import KeyUsageSummary


KMS_KEY_USAGE_LOG_GROUP = os.environ.get("KMS_KEY_USAGE_LOG_GROUP", "/aws/kms/audit")
DEFAULT_SUMMARY_WINDOW_HOURS = 24


def get_key_metadata(key_id: str) -> Dict[str, object]:
    kms_client = get_kms_client()
    resolved_key_id = resolve_key_id(key_id)
    try:
        describe_response = kms_client.describe_key(KeyId=resolved_key_id)
        key_metadata = describe_response["KeyMetadata"]
        key_rotation_status = kms_client.get_key_rotation_status(KeyId=resolved_key_id)
        return {
            "key_id": key_metadata.get("KeyId", ""),
            "key_state": key_metadata.get("KeyState", ""),
            "key_rotation_enabled": key_rotation_status.get(
                "KeyRotationEnabled", False
            ),
            "creation_date": key_metadata.get("CreationDate"),
            "description": key_metadata.get("Description", ""),
            "key_spec": key_metadata.get("KeySpec", ""),
            "key_usage": key_metadata.get("KeyUsage", ""),
        }
    except Exception as e:
        error_info = parse_kms_error(e)
        raise RuntimeError(
            f"AWS KMS DescribeKey failed for {resolved_key_id}: "
            f"[{error_info['error_code']}] {error_info['error_message']}"
        ) from e


def query_kms_cloudtrail_events(
    key_id: str,
    hours: int = DEFAULT_SUMMARY_WINDOW_HOURS,
    region: Optional[str] = None,
) -> List[Dict[str, object]]:
    logs_client = get_cloudwatch_logs_client(region=region)
    resolved_key_id = resolve_key_id(key_id)
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=hours)

    kms_event_names = [
        "Encrypt",
        "Decrypt",
        "GenerateDataKey",
        "GenerateDataKeyWithoutPlaintext",
        "Sign",
        "Verify",
        "DescribeKey",
        "ListKeys",
    ]

    filter_patterns = []
    for event_name in kms_event_names:
        filter_patterns.append(
            f'{{ ($.eventName = "{event_name}") && ($.resources[0].ARN like "*{resolved_key_id}*") }}'
        )

    combined_filter = " || ".join(filter_patterns)

    events = []
    try:
        response = logs_client.filter_log_events(
            logGroupName=KMS_KEY_USAGE_LOG_GROUP,
            startTime=int(start_time.timestamp() * 1000),
            endTime=int(end_time.timestamp() * 1000),
            filterPattern=combined_filter,
            limit=10000,
        )
        for event in response.get("events", []):
            events.append(
                {
                    "timestamp": event.get("timestamp"),
                    "message": event.get("message", ""),
                    "event_id": event.get("eventId", ""),
                }
            )
    except Exception:
        pass

    return events


def summarize_key_usage(
    key_id: str,
    hours: int = DEFAULT_SUMMARY_WINDOW_HOURS,
    region: Optional[str] = None,
) -> KeyUsageSummary:
    metadata = get_key_metadata(key_id)
    events = query_kms_cloudtrail_events(key_id, hours=hours, region=region)

    summary = KeyUsageSummary(
        key_id=metadata["key_id"],
        key_state=metadata["key_state"],
        key_rotation_enabled=metadata["key_rotation_enabled"],
    )

    for event in events:
        message = event.get("message", "")
        if '"Encrypt"' in message:
            summary.total_encryptions += 1
        elif '"Decrypt"' in message:
            summary.total_decryptions += 1
        elif '"Sign"' in message:
            summary.total_signs += 1
        elif '"Verify"' in message:
            summary.total_verifications += 1
        elif '"GenerateDataKey"' in message:
            summary.total_data_key_generations += 1

    if events:
        latest_ts = max(e.get("timestamp", 0) for e in events)
        summary.last_used_timestamp = datetime.fromtimestamp(
            latest_ts / 1000, tz=timezone.utc
        ).isoformat()

    return summary


def format_key_usage_report(
    key_id: str,
    hours: int = DEFAULT_SUMMARY_WINDOW_HOURS,
) -> str:
    summary = summarize_key_usage(key_id, hours=hours)
    report_lines = [
        f"Key Usage Summary for {summary.key_id}",
        f"  Key State: {summary.key_state}",
        f"  Rotation Enabled: {summary.key_rotation_enabled}",
        f"  Last Used: {summary.last_used_timestamp or 'N/A'}",
        f"  Encryptions: {summary.total_encryptions}",
        f"  Decryptions: {summary.total_decryptions}",
        f"  Signs: {summary.total_signs}",
        f"  Verifications: {summary.total_verifications}",
        f"  Data Key Generations: {summary.total_data_key_generations}",
    ]
    return "\n".join(report_lines)
