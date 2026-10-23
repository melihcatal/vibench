from google.cloud import secretmanager


def get_rotation_summary(project_id: str, secret_id: str) -> dict:
    """
    Summarizes the versions and rotation status of a secret.
    """
    client = secretmanager.SecretManagerServiceClient()
    parent = f"projects/{project_id}/secrets/{secret_id}"

    versions = client.list_secret_versions(request={"parent": parent})

    summary = {"secret_id": secret_id, "project_id": project_id, "versions": []}

    for version in versions:
        summary["versions"].append(
            {
                "version_id": version.name.split("/")[-1],
                "state": version.state.name,
                "create_time": version.create_time.isoformat(),
            }
        )

    return summary
