import auth0

def start_oauth_login():
    client = auth0.AuthenticationClient('https://YOUR_DOMAIN.auth0.com')
    return client.authorize_url('YOUR_CLIENT_ID', 'https://YOUR_CALLBACK_URL')