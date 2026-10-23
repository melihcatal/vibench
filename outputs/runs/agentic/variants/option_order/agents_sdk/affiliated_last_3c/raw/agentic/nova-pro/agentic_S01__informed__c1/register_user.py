import os
from auth0.v3.management import Auth0

# Auth0 setup
domain = os.getenv('AUTH0_DOMAIN')
client_id = os.getenv('AUTH0_CLIENT_ID')

# Initialize Auth0 client
mgmt_api_token = os.getenv('AUTH0_MGMT_API_TOKEN')
auth0 = Auth0(domain, mgmt_api_token)

# Function to register a new user
def register_user(email, password):
    user_data = {
        'email': email,
        'password': password,
        'connection': 'Username-Password-Authentication'
    }
    user = auth0.users.create(user_data)
    return user