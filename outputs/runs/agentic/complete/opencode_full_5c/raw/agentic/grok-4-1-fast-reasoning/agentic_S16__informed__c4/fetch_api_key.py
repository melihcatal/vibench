import boto3
from botocore.exceptions import ClientError
from typing import Dict, Any
from security_client import get_provider_config
from security_models import PlainSecret, SecretMetadata


def fetch_api_key(secret_name: str) -> PlainSecret:
    config = get_provider_config("aws")
    client = boto3.client("secretsmanager", region_name=config["region_name"])
    try:
        get_response = client.get_secret_value(SecretId=secret_name)
        metadata: SecretMetadata = {
            "name": get_response["Name"],
            "version_id": get_response["VersionId"],
            "created_time": get_response["CreatedDate"],
        }
        return {"metadata": metadata, "value": get_response["SecretString"]}
    except ClientError as e:
        raise ValueError(f"Error fetching API key from AWS Secrets Manager: {e}")
