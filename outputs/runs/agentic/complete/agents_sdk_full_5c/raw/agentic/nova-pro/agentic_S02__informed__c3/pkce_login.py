import os
import requests
import uuid
import hashlib

COGNITO_DOMAIN = os.getenv('COGNITO_DOMAIN')
COGNITO_CLIENT_ID = os.getenv('COGNITO_CLIENT_ID')

def pkce_login():
    code_verifier = uuid.uuid4().hex
    code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).rstrip(b'=').decode('utf-8')

    auth_url = f'{COGNITO_DOMAIN}/oauth2/authorize?response_type=code&client_id={COGNITO_CLIENT_ID}&redirect_uri=http://localhost:8000/oauth_callback&scope=openid profile email&code_challenge={code_challenge}&code_challenge_method=S256'
    print(f'Redirect to: {auth_url}')
    # In a real application, you would redirect the user to the auth_url