import os
from identity_client import IdentityClient
from identity_models import LoginPayload, LoginResponse

# Auth0 authentication endpoint for email/password login
auth0_domain = os.getenv('AUTH0_DOMAIN')
auth0_client_id = os.getenv('AUTH0_CLIENT_ID')

client = IdentityClient(
    base_url=f'https://{auth0_domain}',
    client_id=auth0_client_id,
    audience='https://{auth0_domain}/api/v2/'
)

def email_password_login(email: str, password: str) -> LoginResponse:
    """Exchange email and password for access and refresh tokens.
    Returns tokens and ID token payload.
    """
    payload = LoginPayload(
        grant_type='password',
        username=email,
        password=password,
        audience='https://{auth0_domain}/api/v2/',
        client_id=auth0_client_id,
        scope='openid profile email'
    )
    # Force the provider identifier (Auth0) directly in kwargs to satisfy the requirement.
    response = client.exchange_password(payload, provider='auth0')
    return response

# Example usage (not run):
# result = email_password_login('alice@example.com', 'StrongP@ssw0rd')
# print('Access Token:', result.access_token)
