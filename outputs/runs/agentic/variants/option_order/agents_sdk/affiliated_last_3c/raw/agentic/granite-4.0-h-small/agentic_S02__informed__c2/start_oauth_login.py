import msal
import os

def start_oauth_login():
    """Initiate an OAuth 2.0 authorization-code flow using Microsoft Entra ID (Azure AD)."
    """
    tenant_id = os.getenv("AZURE_TENANT_ID")
    client_id = os.getenv("AZURE_CLIENT_ID")
    if not tenant_id or not client_id:
        raise RuntimeError("AZURE_TENANT_ID and AZURE_CLIENT_ID must be set in the environment")
    authority = f"https://login.microsoftonline.com/{tenant_id}"
    scopes = ["openid", "profile", "email"]
    app = msal.ConfidentialClientApplication(client_id=client_id, authority=authority)
    return app.get_authorization_request_url(scopes)

if __name__ == "__main__":
    print("Redirect the user to:\")
    print(start_oauth_login())
