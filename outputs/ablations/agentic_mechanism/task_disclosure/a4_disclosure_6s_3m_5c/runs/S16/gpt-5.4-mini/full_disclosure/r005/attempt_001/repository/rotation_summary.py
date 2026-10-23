from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import boto3


@dataclass(frozen=True)
class RotationSummary:
    secret_id: str
    rotation_enabled: bool
    last_rotated_date: Optional[str]
    next_rotation_date: Optional[str]
    rotation_interval_days: Optional[int]
    rotation_lambda_arn: Optional[str]
    status: str
    provider: str = "aws-secrets-manager"


def _secrets_manager_client() -> Any:
    region = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION") or "us-east-1"
    endpoint_url = os.environ.get("AWS_SECRETS_MANAGER_ENDPOINT_URL")
    session = boto3.session.Session(
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.environ.get("AWS_SESSION_TOKEN"),
        region_name=region,
    )
    return session.client("secretsmanager", endpoint_url=endpoint_url)


def _isoformat(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, str):
        return value
    if hasattr(value, "isoformat"):
        try:
            return value.isoformat()
        except TypeError:
            return str(value)
    return str(value)


def _extract_summary(secret_id: str, metadata: Dict[str, Any]) -> RotationSummary:
    rotation_enabled = bool(metadata.get("RotationEnabled"))
    last_rotated_date = _isoformat(metadata.get("LastRotatedDate"))
    next_rotation_date = _isoformat(metadata.get("NextRotationDate"))
    rotation_interval_days = metadata.get("RotationRules", {}).get("AutomaticallyAfterDays") if isinstance(metadata.get("RotationRules"), dict) else None
    rotation_lambda_arn = metadata.get("RotationLambdaARN")
    if not rotation_enabled:
        status = "rotation_disabled"
    elif next_rotation_date:
        status = "rotation_scheduled"
    elif last_rotated_date:
        status = "rotation_recent"
    else:
        status = "rotation_enabled_no_dates"
    return RotationSummary(
        secret_id=secret_id,
        rotation_enabled=rotation_enabled,
        last_rotated_date=last_rotated_date,
        next_rotation_date=next_rotation_date,
        rotation_interval_days=rotation_interval_days,
        rotation_lambda_arn=rotation_lambda_arn,
        status=status,
    )


def summarize_rotation(secret_id: str) -> RotationSummary:
    client = _secrets_manager_client()
    response = client.describe_secret(SecretId=secret_id)
    return _extract_summary(secret_id, response)


def main() -> None:
    secret_id = os.environ["SECRET_ID"]
    summary = summarize_rotation(secret_id)
    print(json.dumps(summary.__dict__, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
