import os
import msal

AUTHORITY = 'https://login.microsoftonline.com/common'
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')

def get_confidential_client():
    return msal.ConfidentialClientApplication(CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET)

def get_public_client():
    return msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)