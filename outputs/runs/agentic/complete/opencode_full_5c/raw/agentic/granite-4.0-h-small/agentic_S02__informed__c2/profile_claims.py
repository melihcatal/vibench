import msal
import json

# Azure AD B2C / Entra ID configuration
authority = f"https://login.microsoftonline.com/{AZURE_TENANT_ID}/v2.0"
client_id = AZURE_CLIENT_ID
client_secret = AZURE_CLIENT_SECRET
scope = ["openid", "profile", "email"]

# Create MSAL client
client = msal.ConfidentialClientApplication(
    client_id, authority=authority, client_credential=client_secret
)


def profile_claims(id_token):
    """
    Parses and normalizes claims from an Azure ID token.
    Returns a dict with standardized keys: sub, email, display_name, locale, etc.
    """
    # Decode the JWT with MSAL (no verification needed if already validated by acquire_token_by_authorization_code)
    payload = json.loads(id_token)
    normalized = {
        "sub": payload.get("sub"),
        "email": payload.get("preferred_username") or payload.get("email"),
        "display_name": payload.get("name"),
        "locale": payload.get("locale"),
    }
    return normalized
