import google.auth
from google.oauth2 import service_account

# Initialize the Google OAuth client
credentials = service_account.Credentials.from_service_account_file(
    'path/to/service-account.json',
    scopes=['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email']
)

# Start the OAuth login flow
auth_url, _ = credentials.authorization_request_url('https://accounts.google.com/o/oauth2/auth')
print(f'Please visit this URL to authorize the application: {auth_url}')

# This script should be run in a context where the user can visit the URL and authorize the application.