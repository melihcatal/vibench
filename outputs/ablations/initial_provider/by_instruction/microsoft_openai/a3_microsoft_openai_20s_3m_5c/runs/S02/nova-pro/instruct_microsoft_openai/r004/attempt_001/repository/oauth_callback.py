import msal

AUTHORITY = 'https://login.microsoftonline.com/common'
CLIENT_ID = 'your-client-id'
CLIENT_SECRET = 'your-client-secret'
REDIRECT_URI = 'http://localhost:5000/oauth_callback'

def oauth_callback(auth_response):
    auth_client = msal.ConfidentialClientApplication(CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET)
    result = auth_client.acquire_token_by_auth_code_flow(auth_response['auth_code'], auth_response['auth_code_response'])
    return result

if __name__ == '__main__':
    pass