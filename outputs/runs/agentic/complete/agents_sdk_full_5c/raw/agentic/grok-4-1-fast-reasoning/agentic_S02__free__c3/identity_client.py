import os
from typing import Optional
from .identity_models import OAuthConfig

def get_google_config() -&gt; OAuthConfig:
    client_id = os.getenv('GOOGLE_CLIENT_ID')
    client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
    redirect_uri = os.getenv('GOOGLE_REDIRECT_URI', 'http://localhost:8080/oauth/callback')
    if not client_id:
        raise ValueError('GOOGLE_CLIENT_ID env var required')
    return OAuthConfig(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scopes=['openid', 'email', 'profile'],
        auth_url='https://accounts.google.com/o/oauth2/v2/auth',
        token_url='https://oauth2.googleapis.com/token',
        userinfo_url='https://openidconnect.googleapis.com/v1/userinfo'
    )

GOOGLE_CONFIG = get_google_config()
