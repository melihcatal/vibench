import os
import auth0

def get_identity_client():
    return auth0.AuthenticationClient(domain=os.getenv('AUTH0_DOMAIN'), client_id=os.getenv('AUTH0_CLIENT_ID'), client_secret=os.getenv('AUTH0_CLIENT_SECRET'))