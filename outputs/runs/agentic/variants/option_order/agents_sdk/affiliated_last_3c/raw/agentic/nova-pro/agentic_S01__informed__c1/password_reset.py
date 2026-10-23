import os
from auth0.v3.management import Auth0

# Auth0 setup
domain = os.getenv('AUTH0_DOMAIN')
client_id = os.getenv('AUTH0_CLIENT_ID')

# Initialize Auth0 client
mgmt_api_token = os.getenv('AUTH0_MGMT_API_TOKEN')
auth0 = Auth0(domain, mgmt_api_token)

# Function to start a password reset flow
def password_reset(email):
    data = {
        'connection': 'Username-Password-Authentication',
        'email': email
    }
    response = auth0.jobs.create('send_email', data)
    return response