from urllib.parse import urlencode
from identity_client import get_auth0_client

def get_authorize_url(session_state: str, connection: str = None) -> str:
    """
    Generates an authorization URL to start the login flow.

    Args:
        session_state: A unique and non-guessable value to be used as the 'state'
                       parameter in the authorization request. It's used to mitigate
                       cross-site request forgery (CSRF) attacks.
        connection: The name of the connection to use for authentication (e.g.,
                    'Username-Password-Authentication', 'google-oauth2'). If not
                    provided, the Auth0 login page will be displayed.

    Returns:
        The URL to redirect the user to for authentication.
    """
    auth0 = get_auth0_client()
    
    # The audience parameter is for requesting an access token for a custom API.
    # Replace 'YOUR_API_IDENTIFIER' with your actual API identifier in Auth0.
    audience = 'https://your-api-identifier.com'
    
    params = {
        'redirect_uri': auth0.redirect_uri,
        'client_id': auth0.client_id,
        'response_type': 'code',
        'scope': 'openid profile email',
        'state': session_state,
        'audience': audience
    }
    if connection:
        params['connection'] = connection

    return f"https://{auth0.domain}/authorize?{urlencode(params)}"
