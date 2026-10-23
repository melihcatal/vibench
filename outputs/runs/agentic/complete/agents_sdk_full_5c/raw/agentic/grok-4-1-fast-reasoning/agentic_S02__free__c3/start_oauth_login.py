import urllib.parse
from .identity_client import GOOGLE_CONFIG
from .identity_models import OAuthConfig

def start_oauth_login(config: OAuthConfig = GOOGLE_CONFIG) -&gt; str:
    params = {
        'client_id': config.client_id,
        'redirect_uri': config.redirect_uri,
        'scope': ' '.join(config.scopes),
        'response_type': 'code',
        'state': 'state_example_123',  # In production, generate securely
    }
    query_string = urllib.parse.urlencode(params)
    auth_url = f"{config.auth_url}?{query_string}"
    return auth_url
