import json

from google.cloud import secretmanager

from security_client import build_secret_version_name, get_secret_manager_client


def parse_json_secret(secret_id: str = "app-config"):
    client: secretmanager.SecretManagerServiceClient = get_secret_manager_client()
    name = build_secret_version_name(secret_id)
    response = client.access_secret_version(request={"name": name})
    return json.loads(response.payload.data.decode("utf-8"))
