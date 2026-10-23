import os
from security_client import SecretManagerHelper
from typing import Dict, Any

# Google Cloud Project ID can be set as an environment variable
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")


def summarize_secret_rotation_status(secret_id: str) -> Dict[str, Any]:
    if not PROJECT_ID:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    client = SecretManagerHelper(project_id=PROJECT_ID)
    versions = client.list_secret_versions(secret_id)

    summary = {
        "secret_id": secret_id,
        "total_versions": len(versions),
        "active_versions": [],
        "destroyed_versions": [],
        "disabled_versions": [],
        "latest_version_create_time": None,
    }

    latest_create_time = None
    for version in versions:
        if version["state"] == "ENABLED":
            summary["active_versions"].append(version)
            if (
                latest_create_time is None
                or version["create_time"] > latest_create_time
            ):
                latest_create_time = version["create_time"]
        elif version["state"] == "DESTROYED":
            summary["destroyed_versions"].append(version)
        elif version["state"] == "DISABLED":
            summary["disabled_versions"].append(version)

    summary["latest_version_create_time"] = latest_create_time

    return summary


# Example Usage (replace with actual secret_id and set GOOGLE_CLOUD_PROJECT_ID env var)
if __name__ == "main":
    try:
        rotation_status = summarize_secret_rotation_status("my-rotating-secret")
        print(f"Rotation Status for {rotation_status['secret_id']}:")
        print(f"  Total Versions: {rotation_status['total_versions']}")
        print(f"  Active Versions: {len(rotation_status['active_versions'])}")
        print(
            f"  Latest Version Create Time: {rotation_status['latest_version_create_time']}"
        )
    except Exception as e:
        print(f"Error summarizing rotation status: {e}")
