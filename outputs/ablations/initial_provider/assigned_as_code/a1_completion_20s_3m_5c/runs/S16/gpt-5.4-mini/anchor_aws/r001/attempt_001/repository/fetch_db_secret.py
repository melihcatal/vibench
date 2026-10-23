import boto3

from security_client import load_config, normalize_secret_value, secret_identifier


def fetch_db_secret(payload, config=None):
    config = load_config(config)
    client = boto3.client("secretsmanager", region_name=config.get("region"))
    response = client.get_secret_value(SecretId=secret_identifier(payload))
    return {"db_secret": normalize_secret_value(response)}
