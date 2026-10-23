import boto3

def summarize_secret_rotation(payload, config=None):
    config = config or {}
    client = boto3.client("secretsmanager", region_name=config.get("region"))
    response = client.describe_secret(SecretId=payload["secret_id"])
    versions = response["VersionIdsToStages"]
    return {"rotation_status": versions}