import json
import os
from typing import Optional


def load_security_config() -> dict:
    config_path = os.environ.get("SECURITY_CONFIG_PATH", "security_config.json")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return json.load(f)
    return {}


def get_aws_credentials() -> dict:
    return {
        "aws_access_key_id": os.environ.get("AWS_ACCESS_KEY_ID", ""),
        "aws_secret_access_key": os.environ.get("AWS_SECRET_ACCESS_KEY", ""),
        "region_name": os.environ.get("AWS_DEFAULT_REGION", "us-east-1"),
    }


def build_secrets_manager_client():
    try:
        import boto3
    except ImportError:
        raise RuntimeError("boto3 is required for AWS Secrets Manager integration")

    credentials = get_aws_credentials()
    session = boto3.Session(
        aws_access_key_id=credentials["aws_access_key_id"],
        aws_secret_access_key=credentials["aws_secret_access_key"],
        region_name=credentials["region_name"],
    )
    return session.client("secretsmanager")


def normalize_secret_name(name: str) -> str:
    return name.strip().lower().replace(" ", "-")


def format_secret_arn(region: str, account_id: str, secret_name: str) -> str:
    return f"arn:aws:secretsmanager:{region}:{account_id}:secret:{secret_name}"


def parse_secret_value(
    secret_string: Optional[str] = None, secret_binary: Optional[bytes] = None
) -> dict:
    if secret_string is not None:
        try:
            return json.loads(secret_string)
        except (json.JSONDecodeError, TypeError):
            return {"raw_value": secret_string}
    if secret_binary is not None:
        return {"raw_binary": secret_binary.decode("utf-8", errors="replace")}
    return {}
