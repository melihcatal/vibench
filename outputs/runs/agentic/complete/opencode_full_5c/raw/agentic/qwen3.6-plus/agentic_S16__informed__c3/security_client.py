import os
from typing import Optional
import boto3
from botocore.config import Config


def get_aws_session() -> boto3.Session:
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID", "")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
    aws_session_token = os.environ.get("AWS_SESSION_TOKEN", "")
    region = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

    session_kwargs = {"region_name": region}
    if aws_access_key_id and aws_secret_access_key:
        session_kwargs["aws_access_key_id"] = aws_access_key_id
        session_kwargs["aws_secret_access_key"] = aws_secret_access_key
    if aws_session_token:
        session_kwargs["aws_session_token"] = aws_session_token

    return boto3.Session(**session_kwargs)


def build_client_config(region: Optional[str] = None) -> Config:
    return Config(
        region_name=region or os.environ.get("AWS_DEFAULT_REGION", "us-east-1"),
        retries={"max_attempts": 3, "mode": "standard"},
    )


def load_secret_env_config() -> dict:
    return {
        "api_key_secret_name": os.environ.get("API_KEY_SECRET_NAME", "prod/api-key"),
        "db_secret_name": os.environ.get(
            "DB_SECRET_NAME", "prod/database/connection-string"
        ),
        "json_secret_name": os.environ.get(
            "JSON_SECRET_NAME", "prod/config/json-payload"
        ),
        "rotation_secret_name": os.environ.get("ROTATION_SECRET_NAME", "prod/api-key"),
        "region": os.environ.get("AWS_DEFAULT_REGION", "us-east-1"),
    }


def normalize_aws_secret_response(raw_response: dict) -> dict:
    return {
        "secret_id": raw_response.get("Name", ""),
        "secret_value": raw_response.get("SecretString", ""),
        "version_id": raw_response.get("VersionId", ""),
        "version_stages": raw_response.get("VersionStages", []),
        "arn": raw_response.get("ARN", ""),
    }
