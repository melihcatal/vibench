from typing import Dict, List
from security_client import GoogleSecretManagerClient
from security_models import SecretResponse


def rotation_summary(secret_ids: List[str]) -> Dict[str, Dict]:
    client = GoogleSecretManagerClient()
    summary = {}

    for secret_id in secret_ids:
        try:
            latest_version = client.get_secret_with_metadata(secret_id)
            previous_version = client.get_secret_with_metadata(
                secret_id, version_id="1"
            )

            summary[secret_id] = {
                "latest_version": {
                    "version_id": latest_version["name"].split("/")[-1],
                    "state": latest_version["state"],
                    "create_time": latest_version["create_time"],
                },
                "previous_version": {
                    "version_id": previous_version["name"].split("/")[-1],
                    "state": previous_version["state"],
                    "create_time": previous_version["create_time"],
                },
                "rotation_status": "ROTATED"
                if latest_version["name"].split("/")[-1] != "1"
                else "NOT_ROTATED",
            }
        except Exception as e:
            summary[secret_id] = {"error": str(e)}

    return summary
