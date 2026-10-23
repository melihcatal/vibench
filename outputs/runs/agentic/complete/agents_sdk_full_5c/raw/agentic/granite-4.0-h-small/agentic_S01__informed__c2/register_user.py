import os
from identity_client import IdentityClient
from identity_models import RegisterRequest, RegisterResponse

# Configuration for Auth0 (environment variables)
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')

def register_user(email: str, password: str, full_name: str = None) -> RegisterResponse:
    """Creates a new email/password user account via Auth0 Management API.
    Returns a normalized RegisterResponse containing user_id and other metadata.
    """
    client = IdentityClient(auth0_domain=AUTH0_DOMAIN,
                            auth0_client_id=AUTH0_CLIENT_ID,
                            auth0_client_secret=AUTH0_CLIENT_SECRET)

    payload = RegisterRequest(
        email=email,
        password=password,
        connection='Username-Password-Authentication',
        user_metadata={'full_name': full_name} if full_name else {}
    )
    response = client.register_user(payload)
    # Normalize response
    normalized = RegisterResponse(
        user_id=response.get('user_id'),
        email=response.get('email'),
        created_at=response.get('created_at'),
        user_metadata=response.get('user_metadata')
    )
    return normalized
