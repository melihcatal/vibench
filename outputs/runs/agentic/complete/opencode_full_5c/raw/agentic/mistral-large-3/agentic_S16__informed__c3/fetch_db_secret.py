import os
import json
from security_client import AWSSecretsClient


def fetch_db_secret(secret_name: str) -> dict:
    client = AWSSecretsClient()
    secret_value = client.get_secret(secret_name)
    return json.loads(secret_value)
