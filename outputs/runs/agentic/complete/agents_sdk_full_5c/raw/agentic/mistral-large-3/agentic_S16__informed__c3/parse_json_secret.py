import json
from security_client import get_secret_manager_client
from security_models import SecretResponse

def parse_json_secret(secret_name: str, version: str = "latest") -> SecretResponse:
    """
    Retrieve and parse a JSON-formatted secret from Google Cloud Secret Manager.
    """
    client = get_secret_manager_client()
    response = client.access_secret_version(request={
        "name": f"projects/{client.project}/secrets/{secret_name}/versions/{version}"
    })
    return SecretResponse(**json.loads(response.payload.data.decode("UTF-8")))