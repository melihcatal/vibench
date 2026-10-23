import os
import boto3
from botocore.config import Config
from typing import Optional


AWS_SECRETS_MANAGER_ENDPOINT = "https://secretsmanager.{region}.amazonaws.com"
DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")


def get_aws_credentials() -> dict:
    return {
        "aws_access_key_id": os.environ.get("AWS_ACCESS_KEY_ID", ""),
        "aws_secret_access_key": os.environ.get("AWS_SECRET_ACCESS_KEY", ""),
        "aws_session_token": os.environ.get("AWS_SESSION_TOKEN", None),
        "region_name": os.environ.get("AWS_DEFAULT_REGION", DEFAULT_REGION),
    }


def create_secrets_manager_client(region: Optional[str] = None) -> boto3.client:
    credentials = get_aws_credentials()
    region_name = region or credentials.pop("region_name")
    config = Config(
        retries={"max_attempts": 3, "mode": "standard"},
        user_agent_extra="SecretMgmtIntegration/1.0",
    )
    endpoint_url = AWS_SECRETS_MANAGER_ENDPOINT.format(region=region_name)
    client = boto3.client(
        "secretsmanager",
        endpoint_url=endpoint_url,
        region_name=region_name,
        config=config,
        **{k: v for k, v in credentials.items() if v is not None},
    )
    return client


def get_secret_value(
    client: boto3.client,
    secret_id: str,
    version_id: Optional[str] = None,
    version_stage: Optional[str] = None,
) -> dict:
    params = {"SecretId": secret_id}
    if version_id:
        params["VersionId"] = version_id
    if version_stage:
        params["VersionStage"] = version_stage
    response = client.get_secret_value(**params)
    return response


def describe_secret(client: boto3.client, secret_id: str) -> dict:
    response = client.describe_secret(SecretId=secret_id)
    return response


def list_secret_version_ids(
    client: boto3.client, secret_id: str, include_deprecated: bool = False
) -> dict:
    params = {"SecretId": secret_id, "IncludeDeprecated": include_deprecated}
    response = client.list_secret_version_ids(**params)
    return response


def rotate_secret(
    client: boto3.client,
    secret_id: str,
    rotation_lambda_arn: Optional[str] = None,
    rotation_rules: Optional[dict] = None,
) -> dict:
    params = {"SecretId": secret_id}
    if rotation_lambda_arn:
        params["RotationLambdaARN"] = rotation_lambda_arn
    if rotation_rules:
        params["RotationRules"] = rotation_rules
    response = client.rotate_secret(**params)
    return response


def put_secret_value(
    client: boto3.client,
    secret_id: str,
    secret_string: str,
    version_stages: Optional[list] = None,
) -> dict:
    params = {
        "SecretId": secret_id,
        "SecretString": secret_string,
    }
    if version_stages:
        params["VersionStages"] = version_stages
    response = client.put_secret_value(**params)
    return response


def validate_environment() -> bool:
    required_vars = ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]
    return all(os.environ.get(var) for var in required_vars)
