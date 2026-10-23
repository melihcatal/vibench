from azure.identity import DefaultAzureCredential


def load_security_config(config=None):
    config = config or {}
    return {
        'key_id': config.get('key_id'),
        'vault_url': config.get('vault_url'),
        'key_name': config.get('key_name'),
        'key_version': config.get('key_version'),
        'note_language': config.get('note_language', 'en'),
    }


def get_credential():
    return DefaultAzureCredential()


def normalize_key_id(config):
    if config.get('key_id'):
        return config['key_id']
    if config.get('vault_url') and config.get('key_name'):
        if config.get('key_version'):
            return f"{config['vault_url'].rstrip('/')}/keys/{config['key_name']}/{config['key_version']}"
        return f"{config['vault_url'].rstrip('/')}/keys/{config['key_name']}"
    return None
