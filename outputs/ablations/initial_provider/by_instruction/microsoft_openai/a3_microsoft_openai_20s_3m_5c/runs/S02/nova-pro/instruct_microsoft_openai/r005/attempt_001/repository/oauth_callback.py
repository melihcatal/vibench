import msal

CLIENT_ID = 'your-client-id'
AUTHORITY = 'https://login.microsoftonline.com/common'
REDIRECT_URI = 'http://localhost:5000/oauth_callback'
SCOPES = ['User.Read']

def oauth_callback(auth_code):
    app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)
    result = app.acquire_token_by_auth_code_flow(auth_code, REDIRECT_URI)
    return result