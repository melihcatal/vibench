import os
from auth0.authentication import Authentication

# Auth0 setup
domain = os.getenv('AUTH0_DOMAIN')
client_id = os.getenv('AUTH0_CLIENT_ID')
client_secret = os.getenv('AUTH0_CLIENT_SECRET')

# Initialize Auth0 client
auth0 = Authentication(domain)

# Function to log in a user with email and password
def email_password_login(email, password):
    data = {
        'grant_type': 'password',
        'username': email,
        'password': password,
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'openid profile email',
        'audience': 'https://' + domain + '/api/v2/'
    }
    response = auth0.oauth_token(data)
    return response.json()