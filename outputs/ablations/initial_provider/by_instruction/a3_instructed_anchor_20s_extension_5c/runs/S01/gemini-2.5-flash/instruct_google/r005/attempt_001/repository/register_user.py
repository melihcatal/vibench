from identity_client import IdentityClient
from identity_models import UserRegistrationRequest

def register_user(email: str, password: str):
    client = IdentityClient()
    request = UserRegistrationRequest(email=email, password=password)
    response = client.register_user(request)
    return response
