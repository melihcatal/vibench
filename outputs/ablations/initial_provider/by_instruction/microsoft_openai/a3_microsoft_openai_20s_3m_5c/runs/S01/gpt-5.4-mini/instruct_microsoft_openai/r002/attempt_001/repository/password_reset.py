from identity_client import IdentityClient
from identity_models import ResetRequest


def password_reset(email: str):
    client = IdentityClient.from_env()
    payload = ResetRequest(email).normalized()
    return client.post("/responses", {"model": "gpt-5.4-mini", "input": [payload]})
