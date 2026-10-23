import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Optional

import boto3


@dataclass(frozen=True)
class RotationSummary:
    secret_name: str
    region_name: str
    enabled: bool
    last_rotated: Optional[str]
    next_rotation: Optional[str]
    version_ids_to_stages: dict[str, list[str]]
    status: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "secret_name": self.secret_name,
            "region_name": self.region_name,
            "enabled": self.enabled,
            "last_rotated": self.last_rotated,
            "next_rotation": self.next_rotation,
            "version_ids_to_stages": self.version_ids_to_stages,
            "status": self.status,
        }


def _parse_time(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc).isoformat()
    if isinstance(value, str):
        return value
    return str(value)


def summarize_secret_rotation(secret_id: Optional[str] = None, region_name: Optional[str] = None) -> RotationSummary:
    secret_name = secret_id or os.environ.get("AWS_SECRET_NAME") or os.environ.get("SECRET_ID")
    if not secret_name:
        raise ValueError("Missing secret id; set AWS_SECRET_NAME or SECRET_ID")
    region = region_name or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    client = boto3.client("secretsmanager", region_name=region)
    response = client.describe_secret(SecretId=secret_name)
    enabled = bool(response.get("RotationEnabled", False))
    version_ids_to_stages = response.get("VersionIdsToStages") or {}
    last_rotated = _parse_time(response.get("LastRotatedDate"))
    next_rotation = _parse_time(response.get("NextRotationDate"))
    if enabled:
        status = "rotating" if next_rotation else "enabled"
    else:
        status = "disabled"
    if version_ids_to_stages and "AWSCURRENT" not in {stage for stages in version_ids_to_stages.values() for stage in stages}:
        status = "stale"
    return RotationSummary(
        secret_name=secret_name,
        region_name=region or "",
        enabled=enabled,
        last_rotated=last_rotated,
        next_rotation=next_rotation,
        version_ids_to_stages={str(version_id): [str(stage) for stage in stages] for version_id, stages in version_ids_to_stages.items()},
        status=status,
    )


def main() -> None:
    summary = summarize_secret_rotation()
    print(summary.to_dict())


if __name__ == "__main__":
    main()
