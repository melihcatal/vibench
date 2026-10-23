import requests

from.identity_client import IdentityClient


def profile_claims(tokens, config=None):
    config = config or {}
    client = IdentityClient(config)
    profile = client.get_profile(tokens['id_token'])
    return profile