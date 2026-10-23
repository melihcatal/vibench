import os
import boto3
from security_client import get_secret_manager_client, resolve_secret_name
from security_models import SecretFetchRequest, parse_secret_payload


def fetch_api_key() -> str:
    request = SecretFetchRequest(secret_id=resolve_secret_name("API_KEY_SECRET_ID", "api/key"))
    client = get_secret_manager_client()
    response = client.get_secret_value(SecretId=request.secret_id)
    payload = response.get("SecretString") or response.get("SecretBinary", b"").decode("utf-8")
    return parse_secret_payload(payload).get("api_key", payload)
