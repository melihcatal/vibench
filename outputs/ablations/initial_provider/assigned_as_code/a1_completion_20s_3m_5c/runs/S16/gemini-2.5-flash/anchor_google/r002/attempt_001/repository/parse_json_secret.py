import json
from google.cloud import secretmanager

def parse_json_secret(project_id, secret_id, version_id="latest"):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    secret_string = response.payload.data.decode("utf-8")
    return json.loads(secret_string)
