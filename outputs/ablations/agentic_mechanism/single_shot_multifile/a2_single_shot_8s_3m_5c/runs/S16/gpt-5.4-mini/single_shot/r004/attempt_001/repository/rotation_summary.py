from collections import Counter
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List

import boto3
from botocore.config import Config


@dataclass(frozen=True)
class RotationSummary:
    total_secrets: int
    by_stage: Dict[str, int]
    by_status: Dict[str, int]


def summarize_rotation_status(secrets: Iterable[Dict[str, Any]]) -> RotationSummary:
    stage_counts = Counter()
    status_counts = Counter()
    total = 0
    for secret in secrets:
        total += 1
        stage = str(secret.get("VersionStages", ["UNKNOWN"])[0]) if secret.get("VersionStages") else "UNKNOWN"
        status = str(secret.get("RotationEnabled", False))
        stage_counts[stage] += 1
        status_counts[status] += 1
    return RotationSummary(total_secrets=total, by_stage=dict(stage_counts), by_status=dict(status_counts))


def list_rotation_candidates(region_name: str) -> List[Dict[str, Any]]:
    client = boto3.client("secretsmanager", region_name=region_name, config=Config(retries={"max_attempts": 3, "mode": "standard"}))
    paginator = client.get_paginator("list_secrets")
    results: List[Dict[str, Any]] = []
    for page in paginator.paginate():
        results.extend(page.get("SecretList", []))
    return results
