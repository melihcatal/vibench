import msal
import json

AUTHORITY = "https://login.microsoftonline.com/common"
CLIENT_ID = "your-client-id"
REDIRECT_URI = "http://localhost:5000/pkce_callback"
SCOPE = ["user.read"]

app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)

def start_pkce_login():
    flow = app.initiate_auth_code_flow(SCOPE, redirect_uri=REDIRECT_URI, code_challenge_method="S256")
    print("Please go to the following URL to login:")
    print(flow['auth_uri'])
    return flow