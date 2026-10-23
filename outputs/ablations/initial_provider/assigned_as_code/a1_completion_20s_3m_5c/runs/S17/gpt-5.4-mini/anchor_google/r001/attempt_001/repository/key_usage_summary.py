from google.cloud import kms

from security_client import load_security_config


def key_usage_summary(payload, config=None):
    config = load_security_config(config)
    client = kms.KeyManagementServiceClient()
    parent = f"projects/{config['project_id']}/locations/{config['location']}"
    keys = client.list_crypto_keys(request={"parent": parent})
    return {"keys": [k.name for k in keys]}
