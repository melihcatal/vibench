from __future__ import annotations

import os
from typing import Dict, List

import boto3

from security_client import load_security_client_config


def summarize_rotation_status(secret_arns: List[str]) -> Dict[str, str]:
    client = boto3.client("secretsmanager", **load_security_client_config().__dict__)
    summary: Dict[str, str] = {}
    for arn in secret_arns:
        meta = client.describe_secret(SecretId=arn)
        summary[arn] = str(meta.get("RotationEnabled", False))
    return summary


if __name__ == "__main__":
    arns = [a for a in os.getenv("ROTATION_SECRET_ARNS", "").split(",") if a]
    print(summarize_rotation_status(arns))
