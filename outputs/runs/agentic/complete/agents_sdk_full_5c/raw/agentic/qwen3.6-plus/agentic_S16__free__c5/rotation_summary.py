"""
rotation_summary.py - Summarize secret rotation status.

Uses AWS Secrets Manager (boto3 SDK) to list secrets, check rotation
configuration, compute overdue status, and generate a rotation summary
report for each managed secret.

Provider: AWS Secrets Manager (secretsmanager.us-east-1.amazonaws.com)
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from botocore.exceptions import ClientError

from security_client import (
    get_secrets_manager_client,
    parse_describe_secret_response,
)
from security_models import (
    SecretMetadata,
    SecretRotationStatus,
    RotationSummary,
    normalize_datetime,
)

logger = logging.getLogger(__name__)


def compute_days_since(dt: Optional[datetime]) -> Optional[int]:
    """Compute the number of days since a given datetime."""
    if dt is None:
        return None
    now = datetime.now(tz=timezone.utc)
    return (now - dt).days


def is_rotation_overdue(
    last_rotated: Optional[datetime],
    interval_days: int,
    next_rotation: Optional[datetime],
) -> bool:
    """Determine if a secret's rotation is overdue."""
    if next_rotation is not None:
        return datetime.now(tz=timezone.utc) > next_rotation
    if last_rotated is not None and interval_days > 0:
        days_since = compute_days_since(last_rotated)
        if days_since is not None:
            return days_since > interval_days
    return False


def get_recommended_action(summary: RotationSummary) -> str:
    """Generate a recommended action based on rotation summary data."""
    if summary.is_overdue:
        return f"URGENT: Rotate immediately. Last rotated {summary.days_since_last_rotation or 'unknown'} days ago."
    if summary.current_status == SecretRotationStatus.PENDING_DELETION:
        return "Secret is pending deletion. Verify this is intentional."
    if not summary.last_rotation:
        return "No rotation history found. Configure rotation if this secret is sensitive."
    if summary.days_since_last_rotation is not None and summary.days_since_last_rotation > 60:
        return "Consider increasing rotation frequency."
    return "Rotation is on schedule. No action needed."


def summarize_secret_rotation(secret_id: str) -> RotationSummary:
    """
    Generate a rotation summary for a single secret from AWS Secrets Manager.

    Args:
        secret_id: The secret name or ARN.

    Returns:
        RotationSummary with rotation status, dates, and recommendations.
    """
    client = get_secrets_manager_client()

    try:
        describe_resp = client.describe_secret(SecretId=secret_id)
        metadata = parse_describe_secret_response(describe_resp)

        last_rotated = metadata.last_rotated_date
        next_rotation = metadata.next_rotation_date
        interval_days = metadata.rotation_interval_days

        overdue = is_rotation_overdue(last_rotated, interval_days, next_rotation)
        days_since = compute_days_since(last_rotated)

        rotation_history = []
        for version_id, stages in describe_resp.get("VersionIdsToStages", {}).items():
            rotation_history.append({
                "version_id": version_id,
                "stages": stages,
            })

        summary = RotationSummary(
            secret_id=metadata.secret_id,
            secret_name=metadata.name,
            current_status=metadata.status,
            last_rotation=last_rotated,
            next_rotation=next_rotation,
            rotation_history=rotation_history,
            is_overdue=overdue,
            days_since_last_rotation=days_since,
        )
        summary.recommended_action = get_recommended_action(summary)
        return summary
    except ClientError as e:
        logger.error("Failed to summarize rotation for %s: %s", secret_id, e)
        return RotationSummary(
            secret_id=secret_id,
            secret_name=secret_id,
            current_status=SecretRotationStatus.UNKNOWN,
            is_overdue=False,
            recommended_action="Could not retrieve rotation status.",
        )


def summarize_all_rotations(
    tag_filter_key: Optional[str] = None,
    tag_filter_value: Optional[str] = None,
) -> List[RotationSummary]:
    """
    Generate rotation summaries for all secrets, optionally filtered by tag.

    Args:
        tag_filter_key: Optional tag key to filter secrets.
        tag_filter_value: Optional tag value to filter secrets.

    Returns:
        List of RotationSummary objects.
    """
    client = get_secrets_manager_client()
    summaries = []

    try:
        list_kwargs: Dict[str, Any] = {}
        if tag_filter_key and tag_filter_value:
            list_kwargs["Filters"] = [
                {"Key": "tag-key", "Values": [tag_filter_key]},
                {"Key": "tag-value", "Values": [tag_filter_value]},
            ]

        paginator = client.get_paginator("list_secrets")
        for page in paginator.paginate(**list_kwargs):
            for secret_entry in page.get("SecretList", []):
                secret_arn = secret_entry.get("ARN", "")
                if secret_arn:
                    summary = summarize_secret_rotation(secret_arn)
                    summaries.append(summary)
    except ClientError as e:
        logger.error("Failed to list secrets for rotation summary: %s", e)

    return summaries


def format_rotation_report(summaries: List[RotationSummary]) -> str:
    """Format a human-readable rotation status report."""
    lines = ["=== Secret Rotation Status Report ===", ""]
    overdue_count = 0

    for s in sorted(summaries, key=lambda x: x.secret_name):
        status_icon = "OVERDUE" if s.is_overdue else "OK"
        if s.is_overdue:
            overdue_count += 1
        lines.append(f"[{status_icon}] {s.secret_name}")
        lines.append(f"  Status: {s.current_status.value}")
        if s.last_rotation:
            lines.append(f"  Last rotated: {s.last_rotation.strftime('%Y-%m-%d')} ({s.days_since_last_rotation or '?'} days ago)")
        if s.next_rotation:
            lines.append(f"  Next rotation: {s.next_rotation.strftime('%Y-%m-%d')}")
        lines.append(f"  Action: {s.recommended_action}")
        lines.append("")

    lines.append(f"Total: {len(summaries)} secrets, {overdue_count} overdue")
    return "\n".join(lines)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    summaries = summarize_all_rotations()
    report = format_rotation_report(summaries)
    print(report)
