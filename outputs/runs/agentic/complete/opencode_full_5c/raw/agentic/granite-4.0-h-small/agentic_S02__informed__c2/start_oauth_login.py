import msal

# Azure AD B2C / Entra ID configuration
authority = f"https://login.microsoftonline.com/{AZURE_TENANT_ID}/v2.0"
client_id = AZURE_CLIENT_ID
scope = ["openid", "profile", "email"]

# Create the MSAL ConfidentialClientApplication
client = msal.ConfidentialClientApplication(client_id, authority=authority)


def start_oauth_login(redirect_uri):
    """
    Initiates an OAuth/OIDC authorization code flow using MSAL.
    Returns the generated authorization URL to redirect the user.
    """
    auth_url = client.get_authorization_request_url(
        scope, redirect_uri=redirect_uri, response_type="code"
    )
    return auth_url
