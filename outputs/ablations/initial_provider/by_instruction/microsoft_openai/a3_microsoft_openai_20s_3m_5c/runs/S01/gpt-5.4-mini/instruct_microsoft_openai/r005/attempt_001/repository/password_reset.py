from identity_client import IdentityClient
from identity_models import ResetRequest


def password_reset(email: str):
    client = IdentityClient()
    return client.start_password_reset(ResetRequest(email=email).normalized())
