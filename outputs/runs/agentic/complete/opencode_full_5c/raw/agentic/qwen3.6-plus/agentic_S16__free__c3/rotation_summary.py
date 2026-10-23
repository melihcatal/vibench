from typing import Optional
from security_models import RotationSummary, RotationStatus
from security_client import get_vault_client


def summarize_rotation(
    secret_path: str, mount_point: Optional[str] = None, rotation_period_days: int = 90
) -> RotationSummary:
    client = get_vault_client()
    try:
        metadata = client.get_rotation_info(secret_path, mount_point)
        versions = metadata.get("versions", {})
        current_version = metadata.get("current_version", 0)

        version_list = sorted(versions.keys(), key=lambda x: int(x))
        previous_version = int(version_list[-2]) if len(version_list) >= 2 else None

        current_ver_info = versions.get(str(current_version), {})
        last_rotated = current_ver_info.get("created_time")

        staged_value = None
        for ver_num, ver_info in versions.items():
            if ver_info.get("status") == "staged":
                staged_value = ver_info
                break

        rotation_status = _compute_rotation_status(
            current_ver_info, rotation_period_days
        )

        return RotationSummary(
            secret_path=secret_path,
            current_version=current_version,
            previous_version=previous_version,
            rotation_status=rotation_status,
            last_rotated=last_rotated,
            next_rotation=_compute_next_rotation(last_rotated, rotation_period_days),
            rotation_period_days=rotation_period_days,
            staged_value=staged_value,
        )
    finally:
        client.close()


def _compute_rotation_status(ver_info: dict, period_days: int) -> RotationStatus:
    import datetime

    created = ver_info.get("created_time")
    if not created:
        return RotationStatus.ACTIVE

    try:
        created_dt = datetime.datetime.fromisoformat(created.replace("Z", "+00:00"))
        age_days = (datetime.datetime.now(datetime.timezone.utc) - created_dt).days
        if age_days > period_days:
            return RotationStatus.EXPIRED
        if age_days > period_days * 0.8:
            return RotationStatus.PENDING
        return RotationStatus.ACTIVE
    except (ValueError, TypeError):
        return RotationStatus.ACTIVE


def _compute_next_rotation(
    created_time: Optional[str], period_days: int
) -> Optional[str]:
    import datetime

    if not created_time:
        return None
    try:
        created_dt = datetime.datetime.fromisoformat(
            created_time.replace("Z", "+00:00")
        )
        next_dt = created_dt + datetime.timedelta(days=period_days)
        return next_dt.isoformat()
    except (ValueError, TypeError):
        return None


if __name__ == "__main__":
    import os

    secret_path = os.environ.get(
        "ROTATION_SECRET_PATH", "prod/database/postgres-primary"
    )
    summary = summarize_rotation(secret_path)
    print(summary.to_dict())
