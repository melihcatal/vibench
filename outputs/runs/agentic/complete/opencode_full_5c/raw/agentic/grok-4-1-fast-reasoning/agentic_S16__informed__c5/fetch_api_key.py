import os
import boto3
from security_client import build_fetched_secret
from security_models import FetchedSecret


def fetch_api_key(secret_name: str) -> FetchedSecret:
    region = os.getenv("AWS_REGION", "us-east-1")
    client = boto3.client(
        "secretsmanager",
        region_name=region,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    response = client.get_secret_value(SecretId=secret_name)
    value = response["SecretString"]
    metadata = {
        "name": secret_name,
        "version_id": response.get("VersionId"),
        "created_date": response.get("CreatedDate"),
    }
    return build_fetched_secret(value, metadata)
