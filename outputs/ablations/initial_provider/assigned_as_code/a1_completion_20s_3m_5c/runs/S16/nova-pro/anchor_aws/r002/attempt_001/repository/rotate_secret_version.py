import boto3

def rotate_secret_version(payload, config=None):
    config = config or {}
    client = boto3.client("secretsmanager", region_name=config.get("region"))
    response = client.get_secret_value(SecretId=payload["secret_id"], VersionStage="AWSCURRENT")
    value = response["SecretString"] if "SecretString" in response else response["SecretBinary"].decode("utf-8")
    return {"secret_version": value}