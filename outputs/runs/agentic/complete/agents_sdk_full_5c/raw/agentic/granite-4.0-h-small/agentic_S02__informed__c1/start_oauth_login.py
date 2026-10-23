import msal
import os

# Microsoft Entra ID (Azure AD) configuration
CLIENT_ID = os.getenv('AZURE_CLIENT_ID')
CLIENT_SECRET = os.getenv('AZURE_CLIENT_SECRET')
TENANT_ID = os.getenv('AZURE_TENANT_ID')
AUTHORITY = f'https://login.microsoftonline.com/{TENANT_ID}'
REDIRECT_URI = 'http://localhost:5000/oauth_callback'

app = msal.ConfidentialClientApplication(
    CLIENT_ID,
    authority=AUTHORITY,
    client_credential=CLIENT_SECRET,
)

def start_oauth_login():
    '''Initiate an OAuth/OIDC authorization-code flow for public client using PKCE.'''
    # Use PKCE flow with msal PublicClientApplication
    public_app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)
    # PKCE parameters
    auth_code_request = {
        'scopes': ['openid', 'profile', 'email'],
        'code_challenge_method': 'S256',
    }
    # get_auth_url is not in msal.PublicClientApplication, use authorize_url from msal library
    auth_url = public_app.get_authorize_url(**auth_code_request)
    print('Please open this URL in your browser and complete login:')
    print(auth_url)

if __name__ == '__main__':
    start_oauth_login()
