import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import requests


@dataclass
class RotationSummary:
    provider: str
    secret_id: str
    version: str
    state: str
    scheduled_rotation_at: Optional[str]
    last_rotated_at: Optional[str]
    summary: str


def _aws_secrets_manager_client_region() -> str:
    return os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"


def _aws_secrets_manager_endpoint(region: str) -> str:
    return f"https://secretsmanager.{region}.amazonaws.com"


def _aws_amz_date() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _aws_date_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d")


def _aws_request_headers(target: str, body: str) -> Dict[str, str]:
    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    session_token = os.getenv("AWS_SESSION_TOKEN")
    if not access_key or not secret_key:
        raise RuntimeError("AWS credentials are required via AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY")

    headers = {
        "Content-Type": "application/x-amz-json-1.1",
        "X-Amz-Target": target,
        "X-Amz-Date": _aws_amz_date(),
    }
    if session_token:
        headers["X-Amz-Security-Token"] = session_token
    return headers


def _fetch_secret_metadata(secret_id: str) -> Dict[str, Any]:
    region = _aws_secrets_manager_client_region()
    endpoint = _aws_secrets_manager_endpoint(region)
    payload = json.dumps({"SecretId": secret_id})
    headers = _aws_request_headers("secretsmanager.DescribeSecret", payload)
    response = requests.post(endpoint, data=payload, headers=headers, timeout=15)
    response.raise_for_status()
    return response.json()


def summarize_rotation_status(secret_id: str) -> RotationSummary:
    metadata = _fetch_secret_metadata(secret_id)
    rotation_enabled = metadata.get("RotationEnabled", False)
    last_rotated_date = metadata.get("LastRotatedDate")
    next_rotation_date = metadata.get("NextRotationDate")
    version_ids_to_stages = metadata.get("VersionIdsToStages", {}) or {}

    current_version = "unknown"
    for version_id, stages in version_ids_to_stages.items():
        if "AWSCURRENT" in stages:
            current_version = version_id
            break

    if rotation_enabled:
        state = "enabled"
    else:
        state = "disabled"

    summary_parts: List[str] = [f"rotation {state}"]
    if last_rotated_date:
        summary_parts.append(f"last rotated {last_rotated_date}")
    if next_rotation_date:
        summary_parts.append(f"next rotation {next_rotation_date}")

    return RotationSummary(
        provider="aws_secrets_manager",
        secret_id=secret_id,
        version=current_version,
        state=state,
        scheduled_rotation_at=next_rotation_date.isoformat() if hasattr(next_rotation_date, "isoformat") else None,
        last_rotated_at=last_rotated_date.isoformat() if hasattr(last_rotated_date, "isoformat") else None,
        summary="; ".join(summary_parts),
    )


def main() -> None:
    secret_id = os.getenv("SECRET_ID")
    if not secret_id:
        raise RuntimeError("SECRET_ID environment variable is required")
    result = summarize_rotation_status(secret_id)
    print(json.dumps(result.__dict__, default=str))


if __name__ == "__main__":
    main()
