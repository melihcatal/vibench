import os


def load_config(config=None):
    base = dict(config or {})
    base.setdefault('vault_url', os.environ['AZURE_KEY_VAULT_URL'])
    return base


def get_secret_name(payload, default_key='secret_id'):
    if default_key in payload:
        return payload[default_key]
    return payload['secret_name']
