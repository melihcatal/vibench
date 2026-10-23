from security_client import SecretManagerClient
from security_models import SecretResponse, normalize_secret_response
import json
import os


def parse_json_secret(secret_id: str = "SERVICE_ACCOUNT_JSON") -> Dict[str, Any]:
    client = SecretManagerClient()
    secret_value = client.get_secret_latest(secret_id)
    version_id = client.list_secret_versions(secret_id)[0]

    parsed_secret = json.loads(secret_value)

    response = normalize_secret_response(
        secret_id=secret_id,
        version_id=version_id,
        secret_value=secret_value,
        labels={"provider": "google-cloud-secret-manager", "type": "json-secret"},
    )

    return {"secret_response": response, "parsed_secret": parsed_secret}
