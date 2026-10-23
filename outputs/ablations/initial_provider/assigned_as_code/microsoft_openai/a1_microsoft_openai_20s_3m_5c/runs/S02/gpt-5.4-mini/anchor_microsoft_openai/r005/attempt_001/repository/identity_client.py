import os

import msal
import requests


def load_identity_config(config=None):
    config = dict(config or {})
    config.setdefault('tenant_id', os.getenv('AZURE_TENANT_ID', 'common'))
    config.setdefault('client_id', os.getenv('AZURE_CLIENT_ID', ''))
    config.setdefault('client_secret', os.getenv('AZURE_CLIENT_SECRET', ''))
    config.setdefault('authority', f"https://login.microsoftonline.com/{config['tenant_id']}")
    config.setdefault('redirect_uri', os.getenv('AZURE_REDIRECT_URI', ''))
    config.setdefault('scopes', ['openid', 'profile', 'email'])
    return config


def build_confidential_app(config=None):
    config = load_identity_config(config)
    return msal.ConfidentialClientApplication(
        config['client_id'],
        authority=config['authority'],
        client_credential=config['client_secret'],
    )


def build_public_app(config=None):
    config = load_identity_config(config)
    return msal.PublicClientApplication(
        config['client_id'],
        authority=config['authority'],
    )


def http_get_json(url, headers=None, timeout=10):
    response = requests.get(url, headers=headers or {}, timeout=timeout)
    response.raise_for_status()
    return response.json()
