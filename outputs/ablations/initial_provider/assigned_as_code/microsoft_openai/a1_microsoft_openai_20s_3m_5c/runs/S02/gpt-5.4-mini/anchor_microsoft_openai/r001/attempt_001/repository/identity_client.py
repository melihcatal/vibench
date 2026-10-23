import os


def load_identity_config(overrides=None):
    overrides = overrides or {}
    config = {
        'tenant_id': os.getenv('AZURE_TENANT_ID', ''),
        'client_id': os.getenv('AZURE_CLIENT_ID', ''),
        'client_secret': os.getenv('AZURE_CLIENT_SECRET', ''),
        'scopes': ['openid', 'profile', 'email', 'User.Read'],
        'profile_url': 'https://graph.microsoft.com/v1.0/me',
    }
    config.update(overrides)
    return config


def merge_identity_payload(payload, config=None):
    config = config or {}
    merged = dict(config)
    merged.update(payload or {})
    return merged
