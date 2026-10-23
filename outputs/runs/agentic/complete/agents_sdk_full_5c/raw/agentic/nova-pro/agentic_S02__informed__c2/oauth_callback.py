import msal
import json

AUTHORITY = "https://login.microsoftonline.com/common"
CLIENT_ID = "your-client-id"
CLIENT_SECRET = "your-client-secret"
REDIRECT_URI = "http://localhost:5000/oauth_callback"

app = msal.ConfidentialClientApplication(CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET)

def handle_callback(auth_result):
    if "access_token" in auth_result:
        print("Login is successful")
        print(json.dumps(auth_result, indent=4))
    else:
        print(auth_result.get("error"))
        print(auth_result.get("error_description"))