from identity_client import IdentityClient
from identity_models import UserLoginRequest

def email_password_login(email: str, password: str):
    client = IdentityClient()
    request = UserLoginRequest(email=email, password=password)
    response = client.sign_in_with_password(request)
    return response
