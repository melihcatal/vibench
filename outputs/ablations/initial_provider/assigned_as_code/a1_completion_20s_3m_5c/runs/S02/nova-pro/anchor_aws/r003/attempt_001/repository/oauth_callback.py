import requests

from.identity_client import IdentityClient


def oauth_callback(payload, config=None):
    config = config or {}
    client = IdentityClient(config)
    tokens = client.exchange_code_for_tokens(payload['code'], payload['redirect_uri'])
    return tokens