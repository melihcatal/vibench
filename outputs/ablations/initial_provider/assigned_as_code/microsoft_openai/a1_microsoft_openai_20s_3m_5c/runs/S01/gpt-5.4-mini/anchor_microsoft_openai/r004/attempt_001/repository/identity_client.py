import os


def load_identity_config(config=None):
    config = config or {}
    return {
        'tenant_id': config.get('tenant_id') or os.environ['AZURE_TENANT_ID'],
        'client_id': config.get('client_id') or os.environ['AZURE_CLIENT_ID'],
        'client_secret': config.get('client_secret') or os.environ['AZURE_CLIENT_SECRET'],
        'issuer': config.get('issuer') or os.environ.get('AZURE_B2C_ISSUER', 'contoso.onmicrosoft.com'),
        'authority_host': config.get('authority_host') or os.environ.get('AZURE_AUTHORITY_HOST', 'https://login.microsoftonline.com'),
        'graph_base_url': config.get('graph_base_url') or os.environ.get('MS_GRAPH_BASE_URL', 'https://graph.microsoft.com/v1.0'),
        'openid_base_url': config.get('openid_base_url') or os.environ.get('AZURE_OPENID_BASE_URL', 'https://login.microsoftonline.com'),
    }


def graph_headers(access_token):
    return {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}


def authority_url(config):
    return f"{config['authority_host'].rstrip('/')}/{config['tenant_id']}"
