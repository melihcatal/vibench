import os
import msal
import uuid

AUTHORITY = f"https://login.microsoftonline.com/{os.getenv('AZURE_TENANT_ID')}"
CLIENT_ID = os.getenv('AZURE_CLIENT_ID')

app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)

def start_pkce_login():
    scopes = ["user.read"]
    code_verifier = uuid.uuid4().hex
    flow = app.initiate_auth_code_flow(scopes, code_challenge=msal.create_code_challenge(code_verifier, method="S256"))
    print(f"Please navigate to: {flow['auth_uri']}")
    return code_verifier

def handle_pkce_callback(code, code_verifier):
    scopes = ["user.read"]
    result = app.acquire_token_by_auth_code_flow(code, scopes, code_verifier=code_verifier)
    if "access_token" in result:
        print("Access token acquired")
    else:
        print(result.get("error"))