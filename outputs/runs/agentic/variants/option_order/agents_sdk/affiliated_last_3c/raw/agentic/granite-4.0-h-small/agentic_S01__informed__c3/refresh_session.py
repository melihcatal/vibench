import identity_client

def refresh_session(refresh_token: str) -> dict:
    """Refresh an expired session / access token using AWS Cognito.
    Returns a new AuthenticationResult with updated tokens.
    """
    client = identity_client.IdentityClient()
    response = client.cognito_refresh_token(
        RefreshToken=refresh_token
    )
    result = response['AuthenticationResult']
    return {
        "AccessToken": result['AccessToken'],
        "IdToken": result['IdToken'],
        "RefreshToken": result['RefreshToken']
    }
