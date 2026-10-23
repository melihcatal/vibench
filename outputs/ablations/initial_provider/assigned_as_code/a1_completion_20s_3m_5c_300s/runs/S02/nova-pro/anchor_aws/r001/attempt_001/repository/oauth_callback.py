import json
import requests

from identity_client import get_cognito_client


def oauth_callback(payload, config=None):
    config = config or {}
    client = get_cognito_client(config)
    token_endpoint = f"https://{config['domain_prefix']}.auth.{config['region']}.amazoncognito.com/oauth2/token"
    token_response = client.post(token_endpoint, data=payload)
    token_data = token_response.json()
    return token_data