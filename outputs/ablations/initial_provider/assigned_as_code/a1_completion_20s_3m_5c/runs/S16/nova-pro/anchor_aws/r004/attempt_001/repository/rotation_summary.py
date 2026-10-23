from security_client import get_secrets_client


def rotation_summary(payload, config=None):
    client = get_secrets_client(config)
    response = client.describe_secret(SecretId=payload["secret_id"])
    versions = response["VersionIdsToStages"]
    summary = {version: stages for version, stages in versions.items()}
    return {"rotation_summary": summary}