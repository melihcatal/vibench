from identity_client import IdentityClient
from identity_models import AccountRequest, coerce_token_response


def email_password_login(email: str, password: str):
    client = IdentityClient()
    payload = client.password_login(AccountRequest(email=email, password=password).normalized())
    return coerce_token_response(payload)
