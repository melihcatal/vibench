
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
            "name": secret.name,
            "rotation_enabled": secret.rotation is not None,
            "next_rotation_time": None
        }
        if secret.rotation:
            rotation_status["next_rotation_time"] = secret.rotation.next_rotation_time.isoformat()
        rotation_summary.append(rotation_status)
    return rotation_summary

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID
    project_id = "your-gcp-project-id"
    summary = summarize_secret_rotation_status(project_id)
    for secret_info in summary:
        print(f"Secret: {secret_info['name']}")
        print(f"  Rotation Enabled: {secret_info['rotation_enabled']}")
        if secret_info['next_rotation_time']:
            print(f"  Next Rotation: {secret_info['next_rotation_time']}")
        print("-" * 20)
