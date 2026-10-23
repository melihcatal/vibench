import os
import json
from security_client import SecurityClient

def parse_json_secret(project_id: str, secret_id: str) -> dict:
    client = SecurityClient()
    json_secret_payload = client.access_secret_version(project_id, secret_id)
    return json.loads(json_secret_payload.data.decode('utf-8'))

if __name__ == '__main__':
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    json_secret_id = "my-json-config-secret"
    # json_config = parse_json_secret(project_id, json_secret_id)
    # print(f"Parsed JSON Secret: {json_config}")
