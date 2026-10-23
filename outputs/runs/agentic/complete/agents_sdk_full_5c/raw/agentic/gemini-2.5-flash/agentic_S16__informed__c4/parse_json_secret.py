from security_client import get_secret_manager_client
from google.api_core.exceptions import NotFound
import json
from security_models import ParsedJsonSecret

def parse_json_secret(project_id: str, secret_id: str) -> ParsedJsonSecret | None:
    """
    Retrieves and parses a JSON-formatted secret from Google Secret Manager.
    """
    client = get_secret_manager_client()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"

    try:
        response = client.access_secret_version(request={"name": name})
        secret_payload = response.payload.data.decode("UTF-8")
        json_data = json.loads(secret_payload)
        return ParsedJsonSecret(name=secret_id, data=json_data)
    except NotFound:
        print(f"Secret {secret_id} not found in project {project_id}.")
        return None
    except json.JSONDecodeError:
        print(f"Secret {secret_id} payload is not valid JSON.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
