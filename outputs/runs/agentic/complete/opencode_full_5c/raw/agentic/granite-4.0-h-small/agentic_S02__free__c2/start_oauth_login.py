import identity_client


def start_oauth_login(provider="Auth0"):
    client = identity_client.get_client(provider)
    # initiate authorization-code flow
    auth_url = client.authorize_url(
        redirect_uri="http://localhost:5000/oauth/callback",
        scope="openid profile email",
    )
    print(f"Redirect user to: {auth_url}")
