import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Define the scopes required for the OAuth flow
SCOPES = ['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email']

def start_oauth_login():
    # Load the client secrets from the environment variable
    client_secrets_file = os.getenv('GOOGLE_CLIENT_SECRETS_FILE')
    if not client_secrets_file:
        raise ValueError('GOOGLE_CLIENT_SECRETS_FILE environment variable is not set.')

    # Create the flow object
    flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)

    # Run the OAuth flow to obtain authorization
    credentials = flow.run_local_server(port=0)

    # Save the credentials for future use
    with open('token.json', 'w') as token:
        token.write(credentials.to_json())

    # Print the obtained credentials
    print('Credentials obtained successfully.')

if __name__ == '__main__':
    start_oauth_login()