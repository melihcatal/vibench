from google.cloud import secretmanager

def rotate_secret_version(project_id: str, secret_id: str, version_to_enable: str) -> None:
    """Read a specific secret version and mark it as the enabled version in Google Secret Manager.

    Args:
        project_id: GCP project identifier.
        secret_id: Identifier of the secret that holds multiple versions.
        version_to_enable: The version string (e.g. '1', 'latest') to promote.

    The function accesses the requested version and then updates the secret's 'replication' policy to
    promote that version as the active one. This demonstrates a rotation/read step.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_to_enable}"
    # Verify the version exists
    client.access_secret_version(name=name)
    # Update the secret's replication to pin this version as the default
    secret_path = f"projects/{project_id}/secrets/{secret_id}"
    client.update_secret(request={
        "secret": {
            "name": secret_path,
            "replication": {
                "automatic": False,  # keep manual rotation control
                "manual": {
                    "replicated_version": version_to_enable
                }
            }
        }
    })
