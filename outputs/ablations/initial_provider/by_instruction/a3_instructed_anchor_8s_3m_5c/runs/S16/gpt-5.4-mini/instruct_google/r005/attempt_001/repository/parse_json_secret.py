import json
import os

from security_client import get_google_secret_manager_client, google_project_id, google_secret_name
from security_models import SecretResponse, normalize_secret_value


def parse_json_secret(secret_id: str = None) -> SecretResponse:
    client = get_google_secret_manager_client()
    project_id = google_project_id()
    secret_id = secret_id or os.environ.get("GOOGLE_JSON_SECRET_ID", "json-secret")
    name = f"{google_secret_name(secret_id, project_id)}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    text = normalize_secret_value(response.payload.data)
    parsed = json.loads(text)
    return SecretResponse(provider="google-secret-manager", secret_id=secret_id, value=json.dumps(parsed), version=response.name, metadata=parsed)
