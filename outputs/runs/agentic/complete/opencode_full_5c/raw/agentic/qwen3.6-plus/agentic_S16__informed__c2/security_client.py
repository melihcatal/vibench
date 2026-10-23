import os
import boto3
from botocore.exceptions import ClientError
from typing import Optional


AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
AWS_DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")


def get_aws_client(region: Optional[str] = None):
    session = boto3.session.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=region or AWS_DEFAULT_REGION,
    )
    client = session.client(service_name="secretsmanager")
    return client


def handle_aws_error(error: Exception, secret_name: str) -> Exception:
    if isinstance(error, ClientError):
        error_code = error.response["Error"]["Code"]
        error_message = error.response["Error"]["Message"]
        if error_code == "ResourceNotFoundException":
            return ValueError(
                f"Secret '{secret_name}' not found in AWS Secrets Manager: {error_message}"
            )
        elif error_code == "InvalidRequestException":
            return ValueError(
                f"Invalid request for secret '{secret_name}': {error_message}"
            )
        elif error_code == "InvalidParameterException":
            return ValueError(
                f"Invalid parameter for secret '{secret_name}': {error_message}"
            )
        elif error_code == "DecryptionFailure":
            return ValueError(
                f"Decryption failed for secret '{secret_name}': {error_message}"
            )
        elif error_code == "AccessDeniedException":
            return PermissionError(
                f"Access denied for secret '{secret_name}': {error_message}"
            )
        else:
            return RuntimeError(
                f"AWS Secrets Manager error for '{secret_name}': {error_message}"
            )
    return RuntimeError(f"Unexpected error accessing secret '{secret_name}': {error}")


def normalize_secret_payload(raw_value: str) -> dict:
    import json

    try:
        return json.loads(raw_value)
    except json.JSONDecodeError:
        return {"raw_value": raw_value}


def build_secret_arn(region: str, account_id: str, secret_name: str) -> str:
    return f"arn:aws:secretsmanager:{region}:{account_id}:secret:{secret_name}"
