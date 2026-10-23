import os
import msal

AUTHORITY = f"https://login.microsoftonline.com/{os.getenv('AZURE_TENANT_ID')}"
CLIENT_ID = os.getenv('AZURE_CLIENT_ID')

app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)

def start_login():
    scopes = ["user.read"]
    flow = app.initiate_auth_code_flow(scopes)
    print(f"Please navigate to: {flow['auth_uri']}")