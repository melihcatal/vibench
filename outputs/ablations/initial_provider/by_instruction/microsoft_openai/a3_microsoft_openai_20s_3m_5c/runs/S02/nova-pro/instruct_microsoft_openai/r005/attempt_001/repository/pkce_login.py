import msal

CLIENT_ID = 'your-client-id'
AUTHORITY = 'https://login.microsoftonline.com/common'
REDIRECT_URI = 'http://localhost:5000/oauth_callback'
SCOPES = ['User.Read']

def pkce_login():
    app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)
    flow = app.initiate_device_flow(SCOPES)
    return flow['device_code']