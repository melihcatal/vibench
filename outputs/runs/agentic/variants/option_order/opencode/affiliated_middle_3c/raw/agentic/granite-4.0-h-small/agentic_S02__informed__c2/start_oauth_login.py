import msal
import os


def start_oauth_login():
    # service: Microsoft Entra OIDC
    # SDK: msal
    # auth: AZURE_TENANT_ID, AZURE_CLIENT_ID
    tenant_id = os.getenv("AZURE_TENANT_ID")
    client_id = os.getenv("AZURE_CLIENT_ID")
    authority = f"https://login.microsoftonline.com/{tenant_id}"
    app = msal.ConfidentialClientApplication(client_id, authority=authority)
    auth_url = app.get_authorization_request_url(["user.read"], response_type="code")
    print("Redirect user to:", auth_url)
