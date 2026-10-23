from google.cloud import secretmanager

def summarize_secret_rotation(project_id: str) -> list[dict]:
    """
    Summarizes secret rotation status by listing secrets and their metadata.

    Args:
        project_id: The Google Cloud project ID.

    Returns:
        A list of dictionaries, each containing secret name and rotation status.
    """
    client = secretmanager.SecretManagerServiceClient()
    parent = f"projects/{project_id}"
    secrets = client.list_secrets(request={"parent": parent})

    summary = []
    for secret in secrets:
        # Simplified: In a real scenario, you'd check rotation schedules, last rotation, etc.
        # Google Cloud Secret Manager doesn't directly expose a 'rotation_status' field.
        # This would typically involve custom labels or external tracking.
        summary.append({
            "name": secret.name,
            "labels": secret.labels,
            "replication_status": str(secret.replication_status.automatic),
            "rotation_enabled": bool(secret.rotation.next_rotation_time) if secret.rotation else False
        })
    return summary
