import os
from auth0.authentication import Authentication

# Auth0 setup
domain = os.getenv('AUTH0_DOMAIN')
client_id = os.getenv('AUTH0_CLIENT_ID')
client_secret = os.getenv('AUTH0_CLIENT_SECRET')

# Initialize Auth0 client
auth0 = Authentication(domain)

# Function to refresh an expired session or access token
def refresh_session(refresh_token):
    data = {
        'grant_type': 'refresh_token',
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token
    }
    response = auth0.oauth_token(data)
    return response.json()