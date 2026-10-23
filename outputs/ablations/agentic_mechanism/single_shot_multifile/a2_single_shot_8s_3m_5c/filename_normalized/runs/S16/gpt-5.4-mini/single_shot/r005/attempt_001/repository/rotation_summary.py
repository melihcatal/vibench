import json
from collections import Counter
from security_models import parse_json_payload
from google.cloud import secretmanager


def summarize_rotation_status(secret_name: str, project_id: str) -> dict:
    client = secretmanager.SecretManagerServiceClient()
    parent = f"projects/{project_id}/secrets/{secret_name}"
    versions = list(client.list_secret_versions(request={"parent": parent}))
    states = Counter(v.state.name for v in versions)
    return {"secret": secret_name, "project_id": project_id, "states": dict(states), "total_versions": len(versions)}
