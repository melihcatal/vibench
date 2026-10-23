from identity_client import auth0_client


def start_oauth_login(redirect_uri: str, state: str):
    request = identity_models.OAuthRequest(redirect_uri, state)
    authorization_url = auth0_client.authorize_url(
        redirect_uri=request.redirect_uri, state=request.state
    )
    print(f"Authorization URL: {authorization_url}")
    return authorization_url
