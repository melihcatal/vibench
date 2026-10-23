import msal
import identity_client


def start_oauth_login(redirect_uri, scopes):
    # Microsoft Entra OIDC example using msal (Microsoft identity platform)
    client_id = identity_client.get_config("AZURE_CLIENT_ID")
    authority = f"https://login.microsoftonline.com/{identity_client.get_config('AZURE_TENANT_ID')}"
    app = msal.ConfidentialClientApplication(client_id, authority=authority)
    auth_url = app.get_authorization_request_url(
        scopes,
        redirect_uri=redirect_uri,
        response_type="code",
        code_challenge_method="S256",
    )
    print("Open this URL in a browser to login:\n", auth_url)
