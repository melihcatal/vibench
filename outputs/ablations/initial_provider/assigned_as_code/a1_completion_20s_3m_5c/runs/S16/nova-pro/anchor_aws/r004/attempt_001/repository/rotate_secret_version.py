from security_client import get_secrets_client


def rotate_secret_version(payload, config=None):
    client = get_secrets_client(config)
    response = client.get_secret_value(SecretId=payload["secret_id"], VersionStage="AWSCURRENT")
    value = response["SecretString"] if "SecretString" in response else response["SecretBinary"].decode("utf-8")
    return {"secret_version": value}