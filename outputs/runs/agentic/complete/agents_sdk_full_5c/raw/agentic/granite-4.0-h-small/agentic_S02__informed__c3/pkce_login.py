import os, random, string, base64, hashlib, requests

def generate_pkce_verifier(length=128):
    # Generate a cryptographically random string for PKCE
    verifier = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    # Encode as base64url without padding for transmission
    verifier_b64 = base64.urlsafe_b64encode(verifier.encode()).decode().rstrip('=')
    return verifier, verifier_b64

def generate_code_verifier(verifier):
    # SHA-256 hash of the verifier for the code_challenge parameter
    hash_bytes = hashlib.sha256(verifier.encode()).digest()
    return base64.urlsafe_b64encode(hash_bytes).decode().rstrip('=')

def start_pkce_login(client_id, redirect_uri, scopes):
    verifier, verifier_b64 = generate_pkce_verifier()
    code_challenge = generate_code_verifier(verifier)
    auth_url = 'https://dev-12345.auth0.com/authorize'
    # Concrete provider: Auth0 using PKCE flow
    params = {
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'scope': ' '.join(scopes),
        'code_challenge': code_challenge,
        'code_challenge_method': 'S256',
        'response_mode': 'query'
    }
    print('Redirect user to:', auth_url, '?', requests.compat.urlencode(params))
    return verifier  # store this securely for token exchange later

def exchange_pkce_for_token(auth_code, redirect_uri, client_id, verifier):
    token_url = 'https://dev-12345.auth0.com/oauth/token'
    payload = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'code_verifier': verifier
    }
    response = requests.post(token_url, data=payload, timeout=10)
    response.raise_for_status()
    return response.json()

if __name__ == '__main__':
    # Example flow using Auth0 as the external OIDC provider
    client_id = os.getenv('AUTH0_CLIENT_ID')
    redirect_uri = 'https://myapp.example.com/callback'
    scopes = ['openid', 'profile', 'email']
    verifier = start_pkce_login(client_id, redirect_uri, scopes)
    # After user authorizes, capture auth_code from callback and run:
    # token_data = exchange_pkce_for_token(auth_code, redirect_uri, client_id, verifier)
