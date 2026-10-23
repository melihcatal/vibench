import os
from datetime import datetime, timezone
from security_client import (
    get_rotation_status,
    describe_secret,
    get_secrets_manager_client,
)
from security_models import RotationStatus


def summarize_rotation_status(secret_id: str = None) -> dict:
    target_id = secret_id or os.environ.get(
        "ROTATION_SECRET_ID", "prod/api/primary-key"
    )
    status = get_rotation_status(target_id)
    metadata = describe_secret(target_id)
    now = datetime.now(timezone.utc)
    days_since_rotation = None
    days_until_rotation = None
    if status.last_rotated_date:
        last_rot = status.last_rotated_date
        if last_rot.tzinfo is None:
            last_rot = last_rot.replace(tzinfo=timezone.utc)
        days_since_rotation = (now - last_rot).days
    if status.next_rotation_date:
        next_rot = status.next_rotation_date
        if next_rot.tzinfo is None:
            next_rot = next_rot.replace(tzinfo=timezone.utc)
        days_until_rotation = (next_rot - now).days
    rotation_interval_days = None
    if status.rotation_rules:
        automatically_after_days = status.rotation_rules.get("AutomaticallyAfterDays")
        if automatically_after_days:
            rotation_interval_days = automatically_after_days
    return {
        "secret_id": target_id,
        "rotation_enabled": status.rotation_enabled,
        "status": _compute_rotation_health(
            status, days_since_rotation, days_until_rotation
        ),
        "last_rotated_date": status.last_rotated_date.isoformat()
        if status.last_rotated_date
        else None,
        "next_rotation_date": status.next_rotation_date.isoformat()
        if status.next_rotation_date
        else None,
        "days_since_last_rotation": days_since_rotation,
        "days_until_next_rotation": days_until_rotation,
        "rotation_interval_days": rotation_interval_days,
        "rotation_lambda_arn": status.rotation_lambda_arn,
        "current_version_stages": status.current_version,
        "tags": metadata.get("Tags", []),
    }


def _compute_rotation_health(
    status: RotationStatus, days_since: int, days_until: int
) -> str:
    if not status.rotation_enabled:
        return "disabled"
    if days_until is not None and days_until < 0:
        return "overdue"
    if days_until is not None and days_until <= 3:
        return "imminent"
    if days_since is not None and status.rotation_rules:
        interval = status.rotation_rules.get("AutomaticallyAfterDays", 30)
        if days_since > interval * 1.5:
            return "stale"
    return "healthy"


def summarize_multiple_secrets(secret_ids: list = None) -> list:
    if secret_ids is None:
        env_val = os.environ.get("SECRET_IDS_LIST", "")
        secret_ids = [s.strip() for s in env_val.split(",") if s.strip()]
    results = []
    for sid in secret_ids:
        try:
            summary = summarize_rotation_status(sid)
            results.append(summary)
        except Exception as e:
            results.append(
                {
                    "secret_id": sid,
                    "error": str(e),
                    "status": "error",
                }
            )
    return results


def rotation_compliance_report(secret_ids: list = None) -> dict:
    summaries = summarize_multiple_secrets(secret_ids)
    enabled_count = sum(1 for s in summaries if s.get("rotation_enabled"))
    healthy_count = sum(1 for s in summaries if s.get("status") == "healthy")
    overdue_count = sum(1 for s in summaries if s.get("status") == "overdue")
    disabled_count = sum(1 for s in summaries if s.get("status") == "disabled")
    return {
        "total_secrets": len(summaries),
        "rotation_enabled": enabled_count,
        "rotation_disabled": disabled_count,
        "healthy": healthy_count,
        "overdue": overdue_count,
        "compliance_rate": healthy_count / len(summaries) if summaries else 0,
        "details": summaries,
    }


if __name__ == "__main__":
    report = summarize_rotation_status()
    print(f"Secret: {report['secret_id']}")
    print(f"Rotation: {report['status']}")
    print(f"Last rotated: {report['last_rotated_date']}")
    print(f"Next rotation: {report['next_rotation_date']}")
