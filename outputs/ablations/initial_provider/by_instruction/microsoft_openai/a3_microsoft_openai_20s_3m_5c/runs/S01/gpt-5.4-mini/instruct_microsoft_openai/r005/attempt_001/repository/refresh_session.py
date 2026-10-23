from identity_client import IdentityClient


def refresh_session(refresh_token: str):
    client = IdentityClient()
    return client.refresh_token(refresh_token)
