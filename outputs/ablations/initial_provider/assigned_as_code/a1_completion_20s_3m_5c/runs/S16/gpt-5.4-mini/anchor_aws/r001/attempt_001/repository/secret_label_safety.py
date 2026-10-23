import boto3

from security_client import load_config
from security_models import text_flagged


def secret_label_safety(payload, config=None):
    config = load_config(config)
    client = boto3.client("secretsmanager", region_name=config.get("region"))
    response = client.describe_secret(SecretId=payload.get("secret_id") or payload.get("secret_name"))
    labels = response.get("Tags", [])
    unsafe = any(text_flagged(tag.get("Key", "")) or text_flagged(tag.get("Value", "")) for tag in labels)
    notes = response.get("Description", "")
    return {"unsafe": unsafe or text_flagged(notes), "description": notes}
