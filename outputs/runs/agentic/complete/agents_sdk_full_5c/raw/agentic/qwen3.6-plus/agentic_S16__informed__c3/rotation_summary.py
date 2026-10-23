"""
rotation_summary.py - Summarize secret rotation status using AWS Secrets Manager
and generate a human-readable summary via Amazon Bedrock (Anthropic Claude model).

Provider 1: AWS Secrets Manager (rotation status data)
Provider 2: Amazon Bedrock Runtime (Anthropic Claude model for summarization)
SDK: boto3
Auth env vars: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
Model ID: anthropic.claude-3-sonnet-20240229-v1:0
"""

import os
import json
import logging
from typing import Optional, List, Dict, Any

import boto3

from security_client import get_secrets_manager_client, retry_with_backoff
from security_models import SecretRotationStatus, normalize_rotation_status

logger = logging.getLogger(__name__)

BEDROCK_REGION = os.environ.get("AWS_REGION", "us-east-1")
BEDROCK_MODEL_ID = os.environ.get(
    "BEDROCK_MODEL_ID",
    "anthropic.claude-3-sonnet-20240229-v1:0",
)


def _bedrock_runtime_client() -> boto3.client:
    """Create a boto3 client for Amazon Bedrock Runtime."""
    return boto3.client(
        "bedrock-runtime",
        region_name=BEDROCK_REGION,
    )


def get_all_secret_names() -> List[str]:
    """List all secret names from AWS Secrets Manager."""
    client = get_secrets_manager_client()
    paginator = client.get_paginator("list_secrets")
    names = []
    for page in paginator.paginate():
        for secret in page.get("SecretList", []):
            name = secret.get("Name", "")
            if name:
                names.append(name)
    return names


def get_rotation_status(secret_name: str) -> SecretRotationStatus:
    """Fetch rotation status for a single secret from AWS Secrets Manager."""
    client = get_secrets_manager_client()

    def _describe():
        return client.describe_secret(SecretId=secret_name)

    raw = retry_with_backoff(_describe)
    return normalize_rotation_status(raw)


def collect_rotation_summaries(
    secret_names: Optional[List[str]] = None,
) -> List[Dict[str, Any]]:
    """
    Collect rotation status for the given secrets (or all secrets if none provided).
    Returns a list of dicts with rotation details.
    """
    if secret_names is None:
        secret_names = get_all_secret_names()

    summaries = []
    for name in secret_names:
        try:
            status = get_rotation_status(name)
            summaries.append(
                {
                    "name": status.name,
                    "arn": status.arn,
                    "rotation_enabled": status.rotation_enabled,
                    "rotation_lambda": status.rotation_lambda_arn,
                    "rotation_rules": status.rotation_rules,
                    "last_rotated": str(status.last_rotated_date),
                }
            )
        except Exception as exc:
            logger.warning("Failed to get rotation status for '%s': %s", name, exc)
            summaries.append(
                {
                    "name": name,
                    "arn": "",
                    "rotation_enabled": False,
                    "error": str(exc),
                }
            )
    return summaries


def generate_rotation_summary_report(
    summaries: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """
    Generate a human-readable rotation status summary using Amazon Bedrock
    (Anthropic Claude model: anthropic.claude-3-sonnet-20240229-v1:0).
    """
    if summaries is None:
        summaries = collect_rotation_summaries()

    data_json = json.dumps(summaries, indent=2, default=str)

    prompt = (
        f"You are a DevOps security engineer. Analyze the following AWS Secrets Manager "
        f"rotation status data and produce a concise summary report. Highlight any secrets "
        f"that do not have rotation enabled, note the rotation cadence, and flag any "
        f"secrets that may need attention.\n\n"
        f"Rotation data:\n{data_json}\n\n"
        f"Provide a structured summary with sections for: Overview, "
        f"Secrets Without Rotation, Rotation Cadence, and Recommendations."
    )

    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 2048,
            "messages": [
                {"role": "user", "content": prompt}
            ],
        }
    )

    bedrock_client = _bedrock_runtime_client()
    response = bedrock_client.invoke_model(
        modelId=BEDROCK_MODEL_ID,
        contentType="application/json",
        accept="application/json",
        body=body,
    )

    result_body = json.loads(response["body"].read().decode("utf-8"))
    summary_text = result_body.get("content", [{}])[0].get("text", "")
    logger.info("Generated rotation summary via Bedrock model %s", BEDROCK_MODEL_ID)
    return summary_text
