import msal

CLIENT_ID = 'your-client-id'
AUTHORITY = 'https://login.microsoftonline.com/common'
REDIRECT_URI = 'http://localhost:5000/oauth_callback'
SCOPES = ['User.Read']

def start_oauth_login():
    app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)
    flow = app.initiate_auth_code_flow(SCOPES, redirect_uri=REDIRECT_URI)
    return flow['auth_uri']