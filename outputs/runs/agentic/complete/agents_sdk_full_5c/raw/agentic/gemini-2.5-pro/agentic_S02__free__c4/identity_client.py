import os
from authlib.integrations.flask_client import OAuth

# Centralized configuration and client factory for identity providers.
# In a real app, this would come from a secure config source.
OKTA_DOMAIN = os.environ.get('OKTA_DOMAIN')
OKTA_CLIENT_ID = os.environ.get('OKTA_CLIENT_ID')
OKTA_CLIENT_SECRET = os.environ.get('OKTA_CLIENT_SECRET')

if not all([OKTA_DOMAIN, OKTA_CLIENT_ID, OKTA_CLIENT_SECRET]):
    raise ValueError("OKTA_DOMAIN, OKTA_CLIENT_ID, and OKTA_CLIENT_SECRET must be set in environment variables.")

# The metadata_url points to Okta's OIDC discovery document
OKTA_METADATA_URL = f'https://{OKTA_DOMAIN}/.well-known/openid-configuration'

oauth = OAuth()

okta_client = oauth.register(
    name='okta',
    client_id=OKTA_CLIENT_ID,
    client_secret=OKTA_CLIENT_SECRET,
    server_metadata_url=OKTA_METADATA_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)
