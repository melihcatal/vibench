import os

from security_client import get_secrets_client, normalize_secret_response


def parse_json_secret(secret_id: str = None):
    client = get_secrets_client()
    secret_id = secret_id or os.getenv("AWS_SECRET_JSON_ID", "app/json")
    response = client.get_secret_value(SecretId=secret_id)
    secret = normalize_secret_response(response)
    return secret.get("SecretString")
