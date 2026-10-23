import boto3

from security_client import load_security_config
from security_models import parse_json_secret_text


def parse_json_secret():
    config = load_security_config("structured/json")
    client = boto3.client("secretsmanager", region_name=config.aws_region)
    response = client.get_secret_value(SecretId=config.secret_id)
    return parse_json_secret_text(response.get("SecretString", "{}"))
