from identity_client import get_auth0_client

def exchange_code_for_tokens(authorization_code: str) -> dict:
    """
    Exchanges an authorization code for an access token, ID token, and refresh token.

    This function is called in the callback handler after the user successfully
    authenticates with the identity provider and is redirected back to the application.

    Args:
        authorization_code: The authorization code received from the identity provider
                           as a query parameter in the callback URL.

    Returns:
        A dictionary containing the access token, ID token, refresh token,
        and other token-related information.
    """
    auth0_get_token = get_auth0_client().get_token
    
    token_payload = {
        'grant_type': 'authorization_code',
        'client_id': auth0_get_token.client_id,
        'client_secret': auth0_get_token.client_secret,
        'code': authorization_code,
        'redirect_uri': auth0_get_token.redirect_uri,
    }
    
    token_info = auth0_get_token.authorization_code(token_payload)
    return token_info
