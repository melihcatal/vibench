import msal
import requests

# Azure AD B2C / Entra ID configuration
authority = f"https://login.microsoftonline.com/{AZURE_TENANT_ID}/v2.0"
client_id = AZURE_CLIENT_ID
client_secret = AZURE_CLIENT_SECRET  # for confidential client
scope = ["openid", "profile", "email"]

# Initialize MSAL ConfidentialClientApplication
client = msal.ConfidentialClientApplication(
    client_id, authority=authority, client_credential=client_secret
)


def oauth_callback(request):
    """
    Handles the OAuth callback request, exchanges authorization code for tokens,
    and returns a dict with 'id_token', 'access_token', and 'refresh_token'.
    Returns None if exchange fails.
    """
    # Expected GET parameters from the callback
    code = request.args.get("code")
    if not code:
        return None

    # Exchange code for tokens
    result = client.acquire_token_by_authorization_code(
        code, scopes=scope, redirect_uri=request.args.get("redirect_uri")
    )
    if "error" in result:
        return None

    tokens = {
        "id_token": result.get("id_token"),
        "access_token": result.get("access_token"),
        "refresh_token": result.get("refresh_token"),
    }
    return tokens
