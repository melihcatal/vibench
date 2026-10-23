from google.cloud import secretmanager
import json
import os

def parse_json_secret(secret_id: str, version_id: str = "latest") -> dict:
    """
    Retrieves and parses a JSON-formatted secret from Google Secret Manager.
    """
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    try:
        response = client.access_secret_version(request={"name": name})
        payload = response.payload.data.decode("UTF-8")
        return json.loads(payload)
    except Exception as e:
        raise RuntimeError(f"Could not retrieve or parse JSON secret {secret_id} from Google Secret Manager: {e}")

