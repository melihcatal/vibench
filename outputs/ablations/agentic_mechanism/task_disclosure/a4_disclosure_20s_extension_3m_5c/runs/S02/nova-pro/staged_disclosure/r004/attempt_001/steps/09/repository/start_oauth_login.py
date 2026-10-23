import os
import google.auth
from google.oauth2 import service_account

# Set up the OAuth 2.0 credentials
credentials = service_account.Credentials.from_service_account_file(
    'path/to/service-account.json',
    scopes=['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email']
)

# Start the OAuth 2.0 flow
auth_requrl = credentials.authorization_request_url()
print('Please go to the following link and authorize access:')
print(auth_requrl)

# Wait for the user to enter the authorization code
auth_code = input('Enter the authorization code: ')

# Exchange the authorization code for tokens
tokens = credentials.exchange_code_for_tokens(auth_code)
print('Access token:', tokens.access_token)
print('Refresh token:', tokens.refresh_token)
