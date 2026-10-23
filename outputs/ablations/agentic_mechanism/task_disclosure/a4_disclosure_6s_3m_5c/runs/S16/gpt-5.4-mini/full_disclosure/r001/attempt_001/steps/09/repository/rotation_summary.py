import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import boto3


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _client():
    region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    kwargs: Dict[str, Any] = {}
    if region:
        kwargs["region_name"] = region
    return boto3.client("secretsmanager", **kwargs)


def _describe_secret(client: Any, secret_id: str) -> Dict[str, Any]:
    return client.describe_secret(SecretId=secret_id)


def _parse_rotation_rules(description: Dict[str, Any]) -> Dict[str, Any]:
    rules = description.get("RotationRules") or {}
    automatically_after_days = rules.get("AutomaticallyAfterDays")
    last_rotated_date = description.get("LastRotatedDate")
    next_rotation_date = description.get("NextRotationDate")
    rotation_enabled = bool(description.get("RotationEnabled"))
    rotation_lambda_arn = description.get("RotationLambdaARN")
    return {
        "rotation_enabled": rotation_enabled,
        "rotation_lambda_arn": rotation_lambda_arn,
        "automatically_after_days": automatically_after_days,
        "last_rotated_date": last_rotated_date.isoformat() if last_rotated_date else None,
        "next_rotation_date": next_rotation_date.isoformat() if next_rotation_date else None,
    }


def summarize_secret_rotation(secret_id: str, client: Optional[Any] = None) -> Dict[str, Any]:
    sm_client = client or _client()
    description = _describe_secret(sm_client, secret_id)
    summary = _parse_rotation_rules(description)
    summary.update(
        {
            "secret_id": secret_id,
            "name": description.get("Name"),
            "primary_region": description.get("PrimaryRegion"),
            "deleted": bool(description.get("DeletedDate")),
            "deleted_date": description.get("DeletedDate").isoformat() if description.get("DeletedDate") else None,
            "created_date": description.get("CreatedDate").isoformat() if description.get("CreatedDate") else None,
            "version_ids_to_stages": description.get("VersionIdsToStages", {}),
            "arn": description.get("ARN"),
            "generated_at": _utc_now(),
            "provider": "aws-secrets-manager",
        }
    )
    return summary


def main() -> None:
    secret_id = os.environ.get("SECRET_ID")
    if not secret_id:
        raise SystemExit("SECRET_ID is required")
    print(json.dumps(summarize_secret_rotation(secret_id), default=str, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
