import boto3
from security_client import get_aws_region, get_secret_name
from security_models import parse_json_payload


def fetch_db_secret(secret_id: str):
    client = boto3.client("secretsmanager", region_name=get_aws_region())
    response = client.get_secret_value(SecretId=get_secret_name(secret_id))
    return parse_json_payload(response.get("SecretString") or response["SecretBinary"])
