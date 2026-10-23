import auth0

def oauth_callback(code):
    client = auth0.AuthenticationClient('https://YOUR_DOMAIN.auth0.com')
    return client.get_token('YOUR_CLIENT_ID', 'YOUR_CLIENT_SECRET', 'https://YOUR_CALLBACK_URL', code)