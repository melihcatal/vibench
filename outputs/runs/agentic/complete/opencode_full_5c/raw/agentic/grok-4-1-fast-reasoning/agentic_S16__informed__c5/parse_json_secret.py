from google.cloud import secretmanager
import os
import json
from security_client import parse_json_secret, build_fetched_secret
from security_models import FetchedSecret


def retrieve_and_parse_json_secret(
    secret_name: str, project_id: str = None
) -> FetchedSecret:
    project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    raw_value = response.payload.data.decode("UTF-8")
    parsed_value = parse_json_secret(raw_value)
    metadata = {
        "name": secret_name,
        "version_id": response.version_id,
        "create_time": str(response.create_time),
    }
    return build_fetched_secret(parsed_value, metadata)
