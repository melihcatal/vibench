import os
from identity_client import IdentityClient
from identity_models import RegisterPayload, RegisterResponse

# Contact Auth0 Management API to create a new email/password user account
auth0_domain = os.getenv('AUTH0_DOMAIN')
auth0_client_id = os.getenv('AUTH0_CLIENT_ID')

client = IdentityClient(
    base_url=f'https://{auth0_domain}',
    client_id=auth0_client_id,
    audience='https://{auth0_domain}/api/v2/'
)

def register_user(email: str, password: str, connection: str = 'Username-Password-Authentication') -> RegisterResponse:
    """Create a new local account using Auth0 Management API.
    Returns the created user object.
    """
    payload = RegisterPayload(
        email=email,
        password=password,
        connection=connection,
        email_verified=False
    )
    response = client.register_user(payload)
    return response

# Example (not executed in library):
# user = register_user('alice@example.com', 'StrongP@ssw0rd')
# print(user)
