import msal

AUTHORITY = 'https://login.microsoftonline.com/common'
CLIENT_ID = 'your-client-id'
REDIRECT_URI = 'http://localhost:5000/callback'
SCOPE = ['User.Read']

def get_pkce_code_challenge():
    cca = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)
    flow = cca.initiate_device_flow(scopes=SCOPE)
    return flow['device_code'], flow['verification_uri_complete']

def get_tokens_from_device_code(device_code):
    cca = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)
    result = cca.acquire_token_by_device_flow(device_code)
    return result