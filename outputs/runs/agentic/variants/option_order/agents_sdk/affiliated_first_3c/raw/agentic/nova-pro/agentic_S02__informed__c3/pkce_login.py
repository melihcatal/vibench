import os
import boto3
import hashlib
import random

cognito_client_id = os.getenv('COGNITO_CLIENT_ID')
cognito_domain = os.getenv('COGNITO_DOMAIN')

def start_pkce_login():
    code_verifier = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=128))
    code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8').rstrip('=')
    authorize_url = f'https://{cognito_domain}/login?response_type=code&client_id={cognito_client_id}&redirect_uri=http://localhost:8000/oauth_callback&code_challenge={code_challenge}&code_challenge_method=S256'
    print(f'Redirect to: {authorize_url}')
    return code_verifier

if __name__ == '__main__':
    start_pkce_login()