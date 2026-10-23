import os
import msal

AUTHORITY = f"https://login.microsoftonline.com/{os.getenv('AZURE_TENANT_ID')}"
CLIENT_ID = os.getenv('AZURE_CLIENT_ID')

app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)

def get_app():
    return app