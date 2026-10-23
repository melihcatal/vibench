import boto3

from security_client import load_security_config
from security_models import normalize_secret_text


def fetch_db_secret() -> str:
    config = load_security_config("database/connection")
    client = boto3.client("secretsmanager", region_name=config.aws_region)
    response = client.get_secret_value(SecretId=config.secret_id)
    return normalize_secret_text(response.get("SecretString", ""))
