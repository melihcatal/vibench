from google.cloud import secretmanager
from security_client import get_secret_manager_client
from security_models import SecretRotationSummary

def summarize_secret_rotation_status(project_id: str):
    client = get_secret_manager_client()
    parent = f"projects/{project_id}"
    secrets_summary = []

    for secret in client.list_secrets(request={"parent": parent}):
        # For simplicity, we are just getting the latest version details
        # A full summary might involve iterating through all versions and checking their states
        try:
            latest_version_name = f"{secret.name}/versions/latest"
            latest_version = client.get_secret_version(request={"name": latest_version_name})

            summary = SecretRotationSummary(
                secret_id=secret.secret_id,
                current_version=str(latest_version.state),
                status="N/A", # More complex logic needed to determine actual rotation status
                create_time=latest_version.create_time.isoformat(),
                destroy_time=latest_version.destroy_time.isoformat() if latest_version.destroy_time else None,
            )
            secrets_summary.append(summary)
        except Exception: # Handle case where a secret might not have a 'latest' version or other issues
            summary = SecretRotationSummary(
                secret_id=secret.secret_id,
                current_version="N/A",
                status="Error/No Version",
                create_time="N/A",
                destroy_time=None,
            )
            secrets_summary.append(summary)

    return {"rotation_summaries": [s.__dict__ for s in secrets_summary]}
