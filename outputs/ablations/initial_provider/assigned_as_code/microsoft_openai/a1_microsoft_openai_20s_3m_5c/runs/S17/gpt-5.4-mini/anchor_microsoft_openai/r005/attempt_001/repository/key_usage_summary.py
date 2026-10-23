import requests

from security_client import load_security_config


def key_usage_summary(payload, config=None):
    config = load_security_config(config)
    response = requests.get(
        "https://management.azure.com/subscriptions",
        headers={"Authorization": f"Bearer {config.get('access_token', '')}"},
        timeout=30,
    )
    return {'summary': response.text, 'provider': 'azure-management'}
