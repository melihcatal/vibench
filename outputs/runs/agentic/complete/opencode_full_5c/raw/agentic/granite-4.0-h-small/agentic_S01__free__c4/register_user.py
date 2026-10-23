import os
from identity_client import IdentityClient
from identity_models import RegisterRequest, RegisterResponse

# Use SendGrid as the concrete provider for user registration
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")


def register_user(email: str, password: str, **kwargs):
    """Create a new email/password user account using SendGrid's Email API.

    Provider identifier: SendGrid (https://sendgrid.com)
    """
    payload = RegisterRequest(email=email, password=password, **kwargs)
    client = IdentityClient(api_key=SENDGRID_API_KEY)
    response = client.register(payload)  # type: RegisterResponse
    # Normalize response to our local model
    return response.to_dict()
