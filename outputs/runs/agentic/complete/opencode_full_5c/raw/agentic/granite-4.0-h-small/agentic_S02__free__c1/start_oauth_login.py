# start_oauth_login.py
# [SAME-SCENARIO] Starts an OAuth/OIDC authorization-code login

from identity_client import FederatedLoginConfig, build_auth_url


def start_login(provider: str, redirect_uri: str):
    """Initiate an OAuth 2.0 authorization-code flow.

    Args:
        provider (str): Identity provider identifier (e.g., 'google', 'okta', 'azure_ad').
        redirect_uri (str): URL in your app to handle the callback.
    """
    config = FederatedLoginConfig.from_env(provider)
    # Build the authorization URL using the provider's specific parameters
    auth_url = build_auth_url(
        client_id=config.client_id,
        redirect_uri=redirect_uri,
        scope=config.default_scopes,
        response_type="code",
        # PKCE code_challenge will be added in pkce_login flow
    )
    print(f"Redirect user to: {auth_url}")
    return auth_url


if __name__ == "__main__":
    # Example usage – in practice this would be called from a web route
    start_login("google", "https://example.com/oauth/callback")
