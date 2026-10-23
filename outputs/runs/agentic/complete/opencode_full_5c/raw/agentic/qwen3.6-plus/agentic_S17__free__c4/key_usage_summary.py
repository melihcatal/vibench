import os
from typing import Optional, List, Dict
from datetime import datetime, timedelta

from security_client import SecurityClient, KMSConfig
from security_models import (
    KeyUsageSummary,
    KeyUsageEvent,
    serialize_event,
)

AWS_KMS_SERVICE_NAME = "kms"
AWS_CLOUDTRAIL_SERVICE_NAME = "cloudtrail"


def get_key_usage_summary(
    key_id: str,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    config: Optional[KMSConfig] = None,
) -> KeyUsageSummary:
    client = SecurityClient(config=config)
    summary = client.build_key_usage_summary(
        key_id=key_id,
        start_time=start_time,
        end_time=end_time,
    )
    return summary


def get_key_usage_summary_last_24h(
    key_id: str,
    config: Optional[KMSConfig] = None,
) -> KeyUsageSummary:
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=24)
    return get_key_usage_summary(
        key_id, start_time=start_time, end_time=end_time, config=config
    )


def get_key_usage_summary_last_7d(
    key_id: str,
    config: Optional[KMSConfig] = None,
) -> KeyUsageSummary:
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=7)
    return get_key_usage_summary(
        key_id, start_time=start_time, end_time=end_time, config=config
    )


def format_usage_summary_report(
    summary: KeyUsageSummary,
) -> str:
    lines = [
        f"Key Usage Summary Report",
        f"========================",
        f"Key ID: {summary.key_id}",
        f"Key ARN: {summary.key_arn}",
        f"Period: {summary.period_start} to {summary.period_end}",
        f"",
        f"Operation Counts:",
        f"  Encryptions: {summary.total_encryptions}",
        f"  Decryptions: {summary.total_decryptions}",
        f"  Signatures: {summary.total_signatures}",
        f"  Verifications: {summary.total_verifications}",
        f"  Data Key Generations: {summary.total_generate_data_key}",
        f"",
        f"Total Events: {len(summary.events)}",
    ]

    if summary.events:
        lines.append("")
        lines.append("Recent Events:")
        for event in summary.events[:10]:
            lines.append(
                f"  - [{event.timestamp}] {event.action} (ID: {event.event_id})"
            )

    return "\n".join(lines)


def summarize_multiple_keys(
    key_ids: List[str],
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    config: Optional[KMSConfig] = None,
) -> Dict[str, KeyUsageSummary]:
    summaries = {}
    for key_id in key_ids:
        try:
            summary = get_key_usage_summary(key_id, start_time, end_time, config)
            summaries[key_id] = summary
        except Exception as e:
            summaries[key_id] = KeyUsageSummary(
                key_id=key_id,
                key_arn="",
                events=[],
            )
    return summaries


def get_crypto_event_timeline(
    key_id: str,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    config: Optional[KMSConfig] = None,
) -> List[Dict]:
    summary = get_key_usage_summary(key_id, start_time, end_time, config)
    timeline = []
    for event in summary.events:
        timeline.append(serialize_event(event))
    timeline.sort(key=lambda x: x.get("timestamp", ""))
    return timeline
