import os
import boto3

COGNITO_DOMAIN = os.getenv('COGNITO_DOMAIN')
COGNITO_CLIENT_ID = os.getenv('COGNITO_CLIENT_ID')

def start_oauth_login():
    login_url = f"https://{COGNITO_DOMAIN}/login?client_id={COGNITO_CLIENT_ID}&response_type=code&scope=openid profile email"
    print(f'Redirect to: {login_url}')"), write_file(path=