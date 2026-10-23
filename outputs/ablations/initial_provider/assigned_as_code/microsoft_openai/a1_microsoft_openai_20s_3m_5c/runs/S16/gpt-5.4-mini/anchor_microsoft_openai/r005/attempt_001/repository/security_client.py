import os


def load_config(config=None):
    base = dict(config or {})
    if 'vault_url' not in base:
        base['vault_url'] = os.environ['AZURE_KEYVAULT_URL']
    return base


def secret_name(payload):
    return payload['secret_id']


def version_name(payload):
    return payload.get('version') or payload.get('secret_version')


def staged_name(payload):
    return payload.get('stage') or payload.get('version_stage')
