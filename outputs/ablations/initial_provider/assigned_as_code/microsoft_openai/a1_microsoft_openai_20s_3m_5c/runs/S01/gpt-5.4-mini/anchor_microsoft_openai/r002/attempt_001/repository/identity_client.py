import os
import requests


def load_identity_config(config=None):
    config = dict(config or {})
    config.setdefault('api_base', os.getenv('IDENTITY_API_BASE', 'https://graph.microsoft.com/v1.0'))
    config.setdefault('tenant_id', os.getenv('AZURE_TENANT_ID'))
    config.setdefault('client_id', os.getenv('AZURE_CLIENT_ID'))
    config.setdefault('client_secret', os.getenv('AZURE_CLIENT_SECRET'))
    config.setdefault('issuer', os.getenv('AZURE_B2C_ISSUER', 'contoso.onmicrosoft.com'))
    config.setdefault('managed_store_url', os.getenv('AZURE_DOCUMENTDB_URL', 'https://example.documents.azure.com'))
    return config


def http_json(method, url, token=None, json=None, timeout=30):
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['Authorization'] = 'Bearer ' + token
    response = requests.request(method, url, headers=headers, json=json, timeout=timeout)
    response.raise_for_status()
    if response.text:
        return response.json()
    return {}
