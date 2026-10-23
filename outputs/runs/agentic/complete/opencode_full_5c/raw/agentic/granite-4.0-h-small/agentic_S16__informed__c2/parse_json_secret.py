import os
import json
from dotenv import load_dotenv

load_dotenv()

# AWS Secrets Manager
import boto3

client = boto3.client("secretsmanager")

from security_models import ParsedSecret


def parse_json_secret(secret_name: str):
    response = client.get_secret_value(SecretId=secret_name)
    secret = json.loads(response["SecretString"])
    # Normalize secret to ParsedSecret object
    return ParsedSecret.from_dict(secret)
