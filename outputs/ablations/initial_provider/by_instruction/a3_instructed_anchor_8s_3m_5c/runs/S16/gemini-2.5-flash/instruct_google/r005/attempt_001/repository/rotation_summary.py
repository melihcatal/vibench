from google.cloud import secretmanager
import os
from typing import List, Dict, Any

def get_secret_rotation_summary(project_id: str) -> List[Dict[str, Any]]:
    """
    Summarizes secret rotation status by listing secrets and their metadata from Google Secret Manager.
    """
    client = secretmanager.SecretManagerServiceClient()
    parent = f"projects/{project_id}"
    
    secrets_summary = []
    for secret in client.list_secrets(request={"parent": parent}):
        # Here we can add more logic to determine rotation status based on secret metadata or labels
        # For now, we'll just return basic info and rotation status if configured.
        rotation_status = "Not Configured"
        if secret.rotation.next_rotation_time and secret.rotation.rotation_period:
            rotation_status = f"Next rotation: {secret.rotation.next_rotation_time.isoformat()}"

        secrets_summary.append({
            "name": secret.name,
            "create_time": secret.create_time.isoformat() if secret.create_time else "N/A",
            "rotation_status": rotation_status,
            "labels": dict(secret.labels)
        })
    return secrets_summary

if __name__ == "__main__":
    # Example usage:
    # project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    # if project_id:
    #     summary = get_secret_rotation_summary(project_id)
    #     for secret_info in summary:
    #         print(f"Secret: {secret_info["name"]}, Status: {secret_info["rotation_status"]}")
    # else:
    #     print("Please set GOOGLE_CLOUD_PROJECT environment variable.")
    pass
