import json
import os
from typing import Optional

from security_client import get_secret_manager_client
from security_models import ParsedJSONSecret


def get_json_secret(project_id: str, secret_id: str) -> Optional[ParsedJSONSecret]:
    """
    Retrieves and parses a JSON-formatted secret from Google Secret Manager.
    """
    client = get_secret_manager_client()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"

    try:
        response = client.access_secret_version(request={"name": name})
        payload = response.payload.data.decode("UTF-8")
        secret_data = json.loads(payload)
        return ParsedJSONSecret(**secret_data)
    except Exception as e:
        print(f"Error parsing JSON secret: {e}")
        return None


if __name__ == "__main__":
    project = os.environ.get("GOOGLE_CLOUD_PROJECT")
    secret = "db-connection-details-json"
    if project:
        parsed_secret = get_json_secret(project, secret)
        if parsed_secret:
            print(f"Successfully parsed secret for host: {parsed_secret.host}")
    else:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
