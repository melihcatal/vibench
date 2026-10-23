import os

AUTHORITY = os.getenv('AUTHORITY')
CLIENT_ID = os.getenv('CLIENT_ID')
REDIRECT_URI = os.getenv('REDIRECT_URI')

def get_client():
    return msal.PublicClientApplication(
        CLIENT_ID, authority=AUTHORITY
    )