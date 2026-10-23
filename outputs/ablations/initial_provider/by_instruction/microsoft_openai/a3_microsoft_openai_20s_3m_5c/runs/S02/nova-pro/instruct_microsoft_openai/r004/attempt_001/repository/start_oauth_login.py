import msal

AUTHORITY = 'https://login.microsoftonline.com/common'
CLIENT_ID = 'your-client-id'
REDIRECT_URI = 'http://localhost:5000/oauth_callback'
SCOPE = ['user.read']

def start_oauth_login():
    auth_client = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)
    flow = auth_client.initiate_auth_code_flow(SCOPE, redirect_uri=REDIRECT_URI)
    auth_url = flow['auth_uri']
    print(f'Please visit {auth_url}')
    return flow

if __name__ == '__main__':
    start_oauth_login()