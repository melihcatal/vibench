import os
from typing import List, Optional
import boto3
from botocore.config import Config

from security_models import RotationStatus
from security_client import get_aws_session, build_client_config


def summarize_rotation_status(
    secret_ids: Optional[List[str]] = None,
) -> List[RotationStatus]:
    region = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

    session = get_aws_session()
    config = build_client_config(region)
    client = session.client("secretsmanager", config=config, region_name=region)

    if secret_ids is None:
        secret_ids = [os.environ.get("ROTATION_SECRET_NAME", "prod/api-key")]

    rotation_statuses: List[RotationStatus] = []

    for secret_id in secret_ids:
        describe_response = client.describe_secret(SecretId=secret_id)

        rotation_rules = describe_response.get("RotationRules", {})
        rotation_lambda = describe_response.get("RotationLambdaARN", "")
        last_changed = describe_response.get("LastChangedDate")
        last_rotated = describe_response.get("LastRotatedDate")

        version_ids = describe_response.get("VersionIdsToStages", {})
        current_version = None
        pending_version = None
        for vid, stages in version_ids.items():
            if "AWSCURRENT" in stages:
                current_version = vid
            if "AWSPENDING" in stages:
                pending_version = vid

        rotation_enabled = bool(rotation_lambda)

        status = RotationStatus(
            secret_id=secret_id,
            rotation_enabled=rotation_enabled,
            last_rotated_date=str(last_rotated) if last_rotated else None,
            next_rotation_date=None,
            rotation_lambda_arn=rotation_lambda if rotation_lambda else None,
            current_version=current_version,
            pending_version=pending_version,
        )
        rotation_statuses.append(status)

    summaries = []
    for s in rotation_statuses:
        rotation_state = "enabled" if s.rotation_enabled else "disabled"
        last_date = s.last_rotated_date or "never"
        pending = s.pending_version or "none"
        summary = (
            f"Secret '{s.secret_id}' rotation is {rotation_state}. "
            f"Last rotated: {last_date}. "
            f"Pending version: {pending}. "
            f"Lambda ARN: {s.rotation_lambda_arn or 'N/A'}."
        )
        summaries.append(summary)

    combined = "\n".join(summaries)

    bedrock_runtime = session.client(
        service_name="bedrock-runtime",
        region_name=region,
        config=config,
    )

    prompt = (
        "You are a security operations assistant. "
        "Summarize the following secret rotation status information in a clear, concise report. "
        "Highlight any secrets that need attention or have pending versions.\n\n"
        f"{combined}"
    )

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
    }

    import json

    response = bedrock_runtime.invoke_model(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        contentType="application/json",
        accept="application/json",
        body=json.dumps(body),
    )

    response_body = json.loads(response.get("body").read())
    summary_text = response_body["content"][0]["text"]

    return {
        "statuses": [s.model_dump() for s in rotation_statuses],
        "summary": summary_text,
    }


if __name__ == "__main__":
    result = summarize_rotation_status()
    import json as _json

    print(_json.dumps(result, indent=2, default=str))
