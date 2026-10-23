import os

AUTHORITY = os.getenv('AZURE_AUTHORITY', 'https://login.microsoftonline.com/common')
CLIENT_ID = os.getenv('AZURE_CLIENT_ID', 'your-client-id')
CLIENT_SECRET = os.getenv('AZURE_CLIENT_SECRET', 'your-client-secret')
REDIRECT_URI = os.getenv('AZURE_REDIRECT_URI', 'http://localhost:5000/oauth_callback')

def get_auth_client():
    return msal.ConfidentialClientApplication(CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET)

if __name__ == '__main__':
    pass