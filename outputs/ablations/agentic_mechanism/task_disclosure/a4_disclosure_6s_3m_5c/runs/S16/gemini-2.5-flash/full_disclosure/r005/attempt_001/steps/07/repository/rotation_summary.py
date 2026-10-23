
from google.cloud import secretmanager

def summarize_secret_rotation_status(project_id: str):
    """
    Summarizes the secret rotation status for a given Google Cloud project.
    """
    client = secretmanager.SecretManagerServiceClient()
    parent = f"projects/{project_id}"

    secrets = client.list_secrets(request={"parent": parent})

    rotation_summary = []
    for secret in secrets:
        rotation_status = {
            "secret_name": secret.name,
            "rotation_enabled": False,
            "rotation_schedule": None
        }
        if secret.replication.automatic is not None and secret.rotation is not None:
            if secret.rotation.next_rotation_time.year != 1970:  # Check if a valid time is set
                rotation_status["rotation_enabled"] = True
                rotation_status["rotation_schedule"] = {
                    "next_rotation_time": secret.rotation.next_rotation_time.isoformat(),
                    "rotation_period": secret.rotation.rotation_period.ToDuration().ToJsonString() if secret.rotation.rotation_period else None
                }
        rotation_summary.append(rotation_status)
    return rotation_summary

if __name__ == '__main__':
    # Replace with your Google Cloud project ID
    # For example: 'your-gcp-project-id'
    project_id = "your-gcp-project-id" 
    
    summary = summarize_secret_rotation_status(project_id)
    import json
    print(json.dumps(summary, indent=2))
