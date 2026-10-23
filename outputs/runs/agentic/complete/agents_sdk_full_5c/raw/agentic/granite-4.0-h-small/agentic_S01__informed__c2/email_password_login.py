import os
from identity_client import IdentityClient
from identity_models import LoginRequest, LoginResponse

# Configuration for Auth0 (environment variables)
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')

def email_password_login(email: str, password: str) -> LoginResponse:
    """Sign in a user via Auth0 using the /oauth/token endpoint and return ID & access tokens."""
    client = IdentityClient(auth0_domain=AUTH0_DOMAIN,
                            auth0_client_id=AUTH0_CLIENT_ID,
                            auth0_client_secret=AUTH0_CLIENT_SECRET)
    payload = LoginRequest(
        client_id=AUTH0_CLIENT_ID,
        username=email,
        password=password,
        grant_type='password',
        audience=f"https://{AUTH0_DOMAIN}/api/v2/",
        scope='openid profile email'
    )
    resp = client.authenticate_with_password_grant(payload)
    # Normalize
    return LoginResponse(
        id_token=resp.get('id_token'),
        access_token=resp.get('access_token'),
        refresh_token=resp.get('refresh_token'),
        expires_in=resp.get('expires_in')
    )
