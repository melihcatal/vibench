from security_client import SecretManagerClient
from typing import Dict, List
import datetime


def rotation_summary(secret_id: str) -> Dict[str, Any]:
    client = SecretManagerClient()
    versions = client.list_secret_versions(secret_id)

    version_details = []
    for version in versions:
        secret_value = client.get_secret_version(secret_id, version)
        version_details.append(
            {
                "version_id": version,
                "state": "ENABLED",
                "created_at": datetime.datetime.now().isoformat(),
                "secret_value_length": len(secret_value),
            }
        )

    return {
        "secret_id": secret_id,
        "provider": "google-cloud-secret-manager",
        "total_versions": len(versions),
        "versions": version_details,
        "last_rotated": version_details[0]["created_at"] if version_details else None,
    }
