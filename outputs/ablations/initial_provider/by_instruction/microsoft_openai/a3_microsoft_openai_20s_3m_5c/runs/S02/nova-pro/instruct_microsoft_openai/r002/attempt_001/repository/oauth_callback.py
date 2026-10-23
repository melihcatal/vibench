import msal

AUTHORITY = 'https://login.microsoftonline.com/common'
CLIENT_ID = 'your-client-id'
CLIENT_SECRET = 'your-client-secret'
REDIRECT_URI = 'http://localhost:5000/callback'

def get_tokens_from_code(code):
    cca = msal.ConfidentialClientApplication(CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET)
    result = cca.acquire_token_by_auth_code_flow(code, redirect_uri=REDIRECT_URI)
    return result