import msal
import identity_client
import requests


def handle_oauth_callback(request):
    # Exchange authorization code for tokens (Microsoft Entra OIDC example)
    client_id = identity_client.get_config("AZURE_CLIENT_ID")
    client_secret = identity_client.get_config("AZURE_CLIENT_SECRET")
    tenant_id = identity_client.get_config("AZURE_TENANT_ID")
    redirect_uri = identity_client.get_config("OAUTH_REDIRECT_URI")
    authority = f"https://login.microsoftonline.com/{tenant_id}"
    app = msal.ConfidentialClientApplication(
        client_id, authority=authority, client_credential=client_secret
    )
    # Parse authorization code from request (e.g., query param 'code')
    code = request.args.get("code")
    if not code:
        raise ValueError("No authorization code provided")
    token_response = app.acquire_token_by_authorization_code(
        code, scopes=[], redirect_uri=redirect_uri
    )
    # token_response now contains 'access_token', 'refresh_token', etc.
    return token_response
