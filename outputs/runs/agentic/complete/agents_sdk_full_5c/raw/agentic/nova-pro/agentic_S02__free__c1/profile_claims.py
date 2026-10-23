import auth0

def profile_claims(access_token):
    client = auth0.AuthenticationClient('https://YOUR_DOMAIN.auth0.com')
    return client.get_userinfo(access_token)