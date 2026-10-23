import auth0

def pkce_login(code_verifier, code_challenge):
    client = auth0.AuthenticationClient('https://YOUR_DOMAIN.auth0.com')
    return client.get_token('YOUR_CLIENT_ID', 'YOUR_CLIENT_SECRET', 'https://YOUR_CALLBACK_URL', code_verifier, code_challenge)