from google.cloud import secretmanager


def rotation_summary(project_id: str) -> str:
    client = secretmanager.SecretManagerServiceClient()
    parent = f"projects/{project_id}"
    summaries = []
    for secret in client.list_secrets(request={"parent": parent}):
        summaries.append(f"{secret.name}:{secret.replication.automatic is not None}")
    return "\n".join(summaries)
