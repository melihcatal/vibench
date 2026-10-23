import os
import boto3

cognito_client_id = os.getenv('COGNITO_CLIENT_ID')
cognito_domain = os.getenv('COGNITO_DOMAIN')

def start_login():
    authorize_url = f'https://{cognito_domain}/login?response_type=code&client_id={cognito_client_id}&redirect_uri=http://localhost:8000/oauth_callback'
    print(f'Redirect to: {authorize_url}')

if __name__ == '__main__':
    start_login()