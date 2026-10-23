import boto3
from security_client import get_aws_region, get_secret_name


def fetch_api_key(secret_id: str) -> str:
    client = boto3.client("secretsmanager", region_name=get_aws_region())
    response = client.get_secret_value(SecretId=get_secret_name(secret_id))
    return response.get("SecretString") or response["SecretBinary"].decode("utf-8")
