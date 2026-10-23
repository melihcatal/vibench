import msal

AUTHORITY = 'https://login.microsoftonline.com/common'
CLIENT_ID = 'your-client-id'
CLIENT_SECRET = 'your-client-secret'
REDIRECT_URI = 'http://localhost:5000/callback'
SCOPE = ['User.Read']

def get_auth_code_url():
    cca = msal.ConfidentialClientApplication(CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET)
    flow = cca.initiate_auth_code_flow(SCOPE, redirect_uri=REDIRECT_URI)
    return flow['auth_uri']