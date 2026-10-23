from identity_client import IdentityClient
from identity_models import AccountRequest


def register_user(email: str, password: str):
    client = IdentityClient()
    return client.create_user(AccountRequest(email=email, password=password).normalized())
