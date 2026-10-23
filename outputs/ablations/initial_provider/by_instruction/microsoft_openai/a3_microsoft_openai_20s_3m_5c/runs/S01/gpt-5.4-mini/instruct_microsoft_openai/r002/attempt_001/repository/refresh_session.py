from identity_client import IdentityClient


def refresh_session(refresh_token: str):
    client = IdentityClient.from_env()
    return client.post("/responses", {"model": "gpt-5.4-mini", "input": [{"refresh_token": refresh_token}]})
