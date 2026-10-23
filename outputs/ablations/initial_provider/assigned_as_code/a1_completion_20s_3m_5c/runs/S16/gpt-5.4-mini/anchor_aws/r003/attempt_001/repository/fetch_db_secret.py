import boto3

from security_client import load_secret_config, normalize_secret_text
from security_models import select_secret_value


def fetch_db_secret(payload, config=None):
    cfg = load_secret_config(config)
    client = boto3.client("secretsmanager", region_name=cfg["region"])
    response = client.get_secret_value(SecretId=payload["secret_id"])
    secret_text = normalize_secret_text(select_secret_value(response))
    return {"db_secret": secret_text}
