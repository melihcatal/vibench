import msal

AUTHORITY = "https://login.microsoftonline.com/common"
CLIENT_ID = "your-client-id"
REDIRECT_URI = "http://localhost:5000/oauth_callback"
SCOPE = ["user.read"]

app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)

def start_login():
    flow = app.initiate_auth_code_flow(SCOPE, redirect_uri=REDIRECT_URI)
    print("Please go to the following URL to login:")
    print(flow['auth_uri'])
    return flow