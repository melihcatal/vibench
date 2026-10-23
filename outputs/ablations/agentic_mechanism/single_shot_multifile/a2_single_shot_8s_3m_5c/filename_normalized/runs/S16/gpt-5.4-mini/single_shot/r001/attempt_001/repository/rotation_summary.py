from typing import Dict, List
from google.cloud import secretmanager


def rotation_summary(accessible_versions: List[str]) -> Dict[str, int]:
    client = secretmanager.SecretManagerServiceClient()
    return {"accessible_versions": len(accessible_versions), "client_type": 1 if client is not None else 0}
