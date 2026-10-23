import os
import boto3
from botocore.config import Config
from typing import Optional, Dict, Any


AWS_KMS_REGION = os.environ.get("AWS_KMS_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
AWS_SESSION_TOKEN = os.environ.get("AWS_SESSION_TOKEN", "")
KMS_ENDPOINT_URL = os.environ.get("KMS_ENDPOINT_URL", "")

DEFAULT_RETRY_CONFIG = Config(
    retries={"max_attempts": 3, "mode": "adaptive"},
    region_name=AWS_KMS_REGION,
)


def get_kms_client(region: Optional[str] = None) -> boto3.client:
    session_kwargs: Dict[str, Any] = {
        "region_name": region or AWS_KMS_REGION,
        "config": DEFAULT_RETRY_CONFIG,
    }
    if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
        session_kwargs["aws_access_key_id"] = AWS_ACCESS_KEY_ID
        session_kwargs["aws_secret_access_key"] = AWS_SECRET_ACCESS_KEY
        if AWS_SESSION_TOKEN:
            session_kwargs["aws_session_token"] = AWS_SESSION_TOKEN
    client = boto3.client("kms", **session_kwargs)
    if KMS_ENDPOINT_URL:
        client.meta.endpoint_url = KMS_ENDPOINT_URL
    return client


def get_cloudwatch_logs_client(region: Optional[str] = None) -> boto3.client:
    session_kwargs: Dict[str, Any] = {
        "region_name": region or AWS_KMS_REGION,
        "config": DEFAULT_RETRY_CONFIG,
    }
    if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
        session_kwargs["aws_access_key_id"] = AWS_ACCESS_KEY_ID
        session_kwargs["aws_secret_access_key"] = AWS_SECRET_ACCESS_KEY
        if AWS_SESSION_TOKEN:
            session_kwargs["aws_session_token"] = AWS_SESSION_TOKEN
    return boto3.client("logs", **session_kwargs)


def resolve_key_id(key_id: str) -> str:
    if key_id.startswith("arn:aws:kms"):
        return key_id
    if key_id.startswith("mrk-"):
        return key_id
    if "-" in key_id and len(key_id) == 36:
        return key_id
    if key_id.startswith("alias/"):
        return key_id
    return f"alias/{key_id}"


def parse_kms_error(exception: Exception) -> Dict[str, Any]:
    error_code = (
        getattr(exception, "response", {}).get("Error", {}).get("Code", "Unknown")
    )
    error_message = (
        getattr(exception, "response", {})
        .get("Error", {})
        .get("Message", str(exception))
    )
    request_id = (
        getattr(exception, "response", {})
        .get("ResponseMetadata", {})
        .get("RequestId", "")
    )
    return {
        "error_code": error_code,
        "error_message": error_message,
        "request_id": request_id,
    }


def validate_aws_credentials() -> bool:
    if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
        try:
            sts = boto3.client("sts", region_name=AWS_KMS_REGION)
            sts.get_caller_identity()
            return True
        except Exception:
            return False
    return True
