import os
import msal

def get_msal_app():
    """Initializes and returns the MSAL ConfidentialClientApplication."""
    client_id = os.environ.get("AZURE_CLIENT_ID")
    client_secret = os.environ.get("AZURE_CLIENT_SECRET")
    tenant_id = os.environ.get("AZURE_TENANT_ID")
    
    authority = f"https://login.microsoftonline.com/{tenant_id}"
    
    app = msal.ConfidentialClientApplication(
        client_id, 
        authority=authority,
        client_credential=client_secret
    )
    return app

def get_msal_public_app():
    """Initializes and returns the MSAL PublicClientApplication for PKCE."""
    client_id = os.environ.get("AZURE_CLIENT_ID")
    tenant_id = os.environ.get("AZURE_TENANT_ID")
    
    authority = f"https://login.microsoftonline.com/{tenant_id}"

    app = msal.PublicClientApplication(
        client_id, 
        authority=authority
    )
    return app


# Configuration for redirect URI
# In a real web app, this would be determined dynamically
REDIRECT_PATH = "/get_a_token" 
SCOPES = ["User.Read"]
