import os


def load_identity_config(config=None):
    config = dict(config or {})
    config.setdefault('client_id', os.getenv('AZURE_CLIENT_ID', ''))
    config.setdefault('tenant_id', os.getenv('AZURE_TENANT_ID', ''))
    config.setdefault('client_secret', os.getenv('AZURE_CLIENT_SECRET', ''))
    config.setdefault('issuer', os.getenv('AZURE_B2C_ISSUER', ''))
    config.setdefault('locale', os.getenv('DEFAULT_LOCALE', 'en'))
    return config


def require_config(config, *keys):
    missing = [key for key in keys if not config.get(key)]
    if missing:
        raise RuntimeError('Missing configuration: ' + ', '.join(missing))
    return config


def graph_headers(access_token):
    return {'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json'}
