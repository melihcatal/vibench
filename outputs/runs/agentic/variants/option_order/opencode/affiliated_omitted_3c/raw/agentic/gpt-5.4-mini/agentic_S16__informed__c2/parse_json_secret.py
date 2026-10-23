import json
import boto3
from security_client import get_secret_manager_client, resolve_secret_name
from security_models import SecretFetchRequest, parse_secret_payload


def parse_json_secret() -> dict:
    request = SecretFetchRequest(secret_id=resolve_secret_name("JSON_SECRET_ID", "app/json-secret"))
    client = get_secret_manager_client()
    response = client.get_secret_value(SecretId=request.secret_id)
    payload = response.get("SecretString") or response.get("SecretBinary", b"").decode("utf-8")
    data = parse_secret_payload(payload)
    return json.loads(json.dumps(data))
