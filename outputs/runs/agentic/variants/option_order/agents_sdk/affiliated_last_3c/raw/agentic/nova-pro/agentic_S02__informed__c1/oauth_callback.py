import os
import msal

AUTHORITY = f"https://login.microsoftonline.com/{os.getenv('AZURE_TENANT_ID')}"
CLIENT_ID = os.getenv('AZURE_CLIENT_ID')

app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)

def handle_callback(code):
    scopes = ["user.read"]
    result = app.acquire_token_by_auth_code_flow(code, scopes)
    if "access_token" in result:
        print("Access token acquired")
    else:
        print(result.get("error"))