import os
import json
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from typing import Optional

from security_models import (
    SecretRequest,
    SecretResponse,
    RotationSummary,
    normalize_secret_name,
    parse_aws_error,
)


AWS_REGION = os.environ.get("AWS_SECRETS_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
AWS_ACCOUNT_ID = os.environ.get("AWS_ACCOUNT_ID", "")
SECRETS_MANAGER_ENDPOINT = os.environ.get(
    "AWS_SECRETS_MANAGER_ENDPOINT",
    f"https://secretsmanager.{AWS_REGION}.amazonaws.com",
)

DEFAULT_RETRY_CONFIG = Config(
    retries={"max_attempts": 3, "mode": "standard"},
    connect_timeout=5,
    read_timeout=10,
)


def get_secrets_manager_client(region: Optional[str] = None):
    client_region = region or AWS_REGION
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=client_region,
    )
    return session.client("secretsmanager", config=DEFAULT_RETRY_CONFIG)


def fetch_secret_value(
    secret_name: str,
    version_id: Optional[str] = None,
    version_stage: Optional[str] = None,
    region: Optional[str] = None,
) -> SecretResponse:
    client = get_secrets_manager_client(region)
    kwargs = {"SecretId": secret_name}
    if version_id:
        kwargs["VersionId"] = version_id
    if version_stage:
        kwargs["VersionStage"] = version_stage

    response = client.get_secret_value(**kwargs)

    secret_value = response.get("SecretString") or response.get(
        "SecretBinary", b""
    ).decode("utf-8", errors="replace")

    return SecretResponse(
        secret_name=response["Name"],
        secret_value=secret_value,
        version_id=response.get("VersionId"),
        version_stages=response.get("VersionStages", []),
        created_date=response.get("CreatedDate", "").isoformat()
        if response.get("CreatedDate")
        else None,
    )


def describe_secret(secret_name: str, region: Optional[str] = None) -> dict:
    client = get_secrets_manager_client(region)
    response = client.describe_secret(SecretId=secret_name)
    return response


def list_secret_version_ids(secret_name: str, region: Optional[str] = None) -> list:
    client = get_secrets_manager_client(region)
    response = client.list_secret_version_ids(
        SecretId=secret_name, IncludeDeprecated=True
    )
    return response.get("Versions", [])


def build_rotation_summary(
    secret_name: str, region: Optional[str] = None
) -> RotationSummary:
    desc = describe_secret(secret_name, region)
    rotation_rules = desc.get("RotationRules", {})
    rotation_lambda = desc.get("RotationLambdaARN")
    last_rotated = desc.get("LastRotatedDate")
    next_rotation = desc.get("NextRotationDate")
    last_changed = desc.get("LastChangedDate")

    version_stages_summary = {}
    try:
        versions = list_secret_version_ids(secret_name, region)
        for v in versions:
            stage = (
                "deprecated" if v.get("VersionStages") == ["AWSPREVIOUS"] else "current"
            )
            version_stages_summary[v.get("VersionId", "")] = {
                "stage": stage,
                "created": v.get("CreatedDate", "").isoformat()
                if v.get("CreatedDate")
                else None,
            }
    except Exception:
        pass

    rotation_enabled = desc.get("RotationEnabled", False)
    rotation_status = "enabled" if rotation_enabled else "disabled"

    summary_lines = [
        f"Secret: {secret_name}",
        f"Rotation: {rotation_status}",
    ]
    if rotation_lambda:
        summary_lines.append(f"Lambda: {rotation_lambda}")
    if rotation_rules:
        summary_lines.append(f"Rules: {json.dumps(rotation_rules)}")
    if last_rotated:
        summary_lines.append(f"Last rotated: {last_rotated.isoformat()}")
    if next_rotation:
        summary_lines.append(f"Next rotation: {next_rotation.isoformat()}")

    return RotationSummary(
        secret_name=secret_name,
        rotation_enabled=rotation_enabled,
        rotation_lambda_arn=rotation_lambda,
        rotation_rules=rotation_rules,
        last_rotation_status=rotation_status,
        last_rotation_date=last_rotated.isoformat() if last_rotated else None,
        next_rotation_date=next_rotation.isoformat() if next_rotation else None,
        version_stages_summary=version_stages_summary,
        summary_text="\n".join(summary_lines),
    )


def handle_aws_error(error: ClientError) -> dict:
    error_code = error.response["Error"]["Code"]
    error_message = error.response["Error"]["Message"]
    return parse_aws_error(error_code, error_message)


def get_openai_client():
    import openai

    return openai.OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY", ""),
        base_url=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    )


def create_openai_completion(
    messages: list,
    model: str = "gpt-4o-mini",
    temperature: float = 0.0,
    max_tokens: int = 1024,
) -> str:
    client = get_openai_client()
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content


def create_openai_embedding(
    text: str,
    model: str = "text-embedding-3-small",
    dimensions: int = 256,
) -> list:
    client = get_openai_client()
    response = client.embeddings.create(
        model=model,
        input=text,
        dimensions=dimensions,
    )
    return response.data[0].embedding
