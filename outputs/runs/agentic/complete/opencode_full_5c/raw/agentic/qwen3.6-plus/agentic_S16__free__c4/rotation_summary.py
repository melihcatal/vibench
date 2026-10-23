import os
from datetime import datetime, timezone
from security_client import create_secrets_manager_client, describe_secret
from security_models import RotationStatus, build_aws_secret_request


def summarize_rotation_status(secret_id: str, region: str = None) -> dict:
    request = build_aws_secret_request(secret_id, region=region)
    client = create_secrets_manager_client(region=request.region)
    aws_response = describe_secret(client, request.secret_id)
    rotation_status = RotationStatus.from_aws_describe(request.secret_id, aws_response)
    summary = build_rotation_summary(rotation_status, aws_response)
    return summary


def build_rotation_summary(status: RotationStatus, raw_aws_response: dict) -> dict:
    now = datetime.now(timezone.utc)
    rotation_enabled = status.rotation_enabled
    last_rotated = status.last_rotated_date
    next_rotation = status.next_rotation_date

    days_since_rotation = None
    days_until_rotation = None

    if last_rotated and last_rotated != "":
        try:
            last_dt = datetime.fromisoformat(last_rotated.replace("Z", "+00:00"))
            days_since_rotation = (now - last_dt).days
        except (ValueError, TypeError):
            pass

    if next_rotation and next_rotation != "":
        try:
            next_dt = datetime.fromisoformat(next_rotation.replace("Z", "+00:00"))
            days_until_rotation = (next_dt - now).days
        except (ValueError, TypeError):
            pass

    has_pending_version = (
        status.pending_version is not None and status.pending_version != ""
    )

    rotation_health = "healthy"
    if rotation_enabled and days_since_rotation is not None:
        auto_days = status.rotation_rules.get("automatically_after_days")
        if auto_days and days_since_rotation > auto_days:
            rotation_health = "overdue"
        elif auto_days and days_since_rotation > auto_days * 0.8:
            rotation_health = "warning"

    return {
        "secret_id": status.secret_id,
        "rotation_enabled": rotation_enabled,
        "rotation_health": rotation_health,
        "last_rotated_date": last_rotated,
        "next_rotation_date": next_rotation,
        "days_since_last_rotation": days_since_rotation,
        "days_until_next_rotation": days_until_rotation,
        "rotation_lambda_arn": status.rotation_lambda_arn,
        "rotation_schedule": status.rotation_rules.get("schedule_expression")
        or f"every {status.rotation_rules.get('automatically_after_days', 'N/A')} days",
        "has_pending_version": has_pending_version,
        "current_version_id": status.current_version,
        "pending_version_id": status.pending_version,
        "raw_tags": raw_aws_response.get("Tags", []),
    }


def summarize_multiple_secrets(secret_ids: list, region: str = None) -> list:
    summaries = []
    for sid in secret_ids:
        try:
            summary = summarize_rotation_status(sid, region=region)
            summaries.append(summary)
        except Exception as e:
            summaries.append(
                {
                    "secret_id": sid,
                    "error": str(e),
                    "rotation_enabled": False,
                    "rotation_health": "error",
                }
            )
    return summaries


if __name__ == "__main__":
    secret_id = os.environ.get("ROTATION_SUMMARY_SECRET_ID", "prod/api/payment-key")
    result = summarize_rotation_status(secret_id)
    print(result)
