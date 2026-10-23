import msal
import identity_client


def start_pkce_login(redirect_uri, scopes):
    # Public client (PKCE) flow using msal (Microsoft identity platform) as an example
    client_id = identity_client.get_config("AZURE_CLIENT_ID")
    authority = f"https://login.microsoftonline.com/{identity_client.get_config('AZURE_TENANT_ID')}"
    app = msal.PublicClientApplication(client_id, authority=authority)
    # Generate PKCE code verifier and challenge
    code_verifier = msal.core.crypto.random_string(length=128)
    code_challenge = msal.core.crypto.sha256(code_verifier)
    # Build authorization URL with code_challenge and method
    auth_url = app.get_authorization_request_url(
        scopes,
        redirect_uri=redirect_uri,
        response_type="code",
        code_challenge=code_challenge,
        code_challenge_method="S256",
    )
    print("Open this URL in a browser to login (PKCE):", auth_url)
    return code_verifier  # Store for later exchange
