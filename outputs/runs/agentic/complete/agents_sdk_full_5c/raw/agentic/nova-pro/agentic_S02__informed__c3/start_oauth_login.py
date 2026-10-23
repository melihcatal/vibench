import os
import requests

COGNITO_DOMAIN = os.getenv('COGNITO_DOMAIN')
COGNITO_CLIENT_ID = os.getenv('COGNITO_CLIENT_ID')

def start_oauth_login():
    auth_url = f'{COGNITO_DOMAIN}/oauth2/authorize?response_type=code&client_id={COGNITO_CLIENT_ID}&redirect_uri=http://localhost:8000/oauth_callback&scope=openid profile email'
    print(f'Redirect to: {auth_url}')
    # In a real application, you would redirect the user to the auth_url