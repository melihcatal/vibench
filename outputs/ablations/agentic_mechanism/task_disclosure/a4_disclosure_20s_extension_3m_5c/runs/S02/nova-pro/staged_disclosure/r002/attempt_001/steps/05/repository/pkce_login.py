import requests

AUTH0_DOMAIN = 'your-auth0-domain.auth0.com'
CLIENT_ID = 'your-client-id'
REDIRECT_URI = 'http://localhost:3000/callback'

def generate_code_verifier():
    # Generate a random string of bytes
    code_verifier = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=64))
    return code_verifier

def generate_code_challenge(code_verifier):
    # Generate the code challenge from the code verifier
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest()).decode().rstrip('=\n')
    return code_challenge

def get_authorization_url(code_challenge):
    # Construct the authorization URL
    auth_url = f'https://{AUTH0_DOMAIN}/authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&code_challenge={code_challenge}&code_challenge_method=S256'
    return auth_url

def get_tokens(code, code_verifier):
    # Exchange the authorization code for tokens
    token_url = f'https://{AUTH0_DOMAIN}/oauth/token'
    data = {
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'code_verifier': code_verifier
    }
    response = requests.post(token_url, data=data)
    response.raise_for_status()
    return response.json()

if __name__ == '__main__':
    import base64
    import hashlib
    import random
    
    code_verifier = generate_code_verifier()
    code_challenge = generate_code_challenge(code_verifier)
    
    auth_url = get_authorization_url(code_challenge)
    print(f'Please visit this URL to authorize: {auth_url}')
    
    # After authorization, the user will be redirected to the redirect_uri with a code
    # For example: http://localhost:3000/callback?code=AUTHORIZATION_CODE
    # Extract the code from the redirect URL
    code = input('Enter the code from the redirect URL: ')
    
    tokens = get_tokens(code, code_verifier)
    print('Access Token:', tokens['access_token'])
    print('ID Token:', tokens['id_token'])
    print('Refresh Token:', tokens['refresh_token'] if 'refresh_token' in tokens else 'N/A')
