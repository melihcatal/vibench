import os
import base64
import hashlib
from identity_models import OAuthConfig, PKCEParams


def get_okta_config():
    return OAuthConfig(
        client_id=os.environ.get("OKTA_CLIENT_ID"),
        client_secret=os.environ.get("OKTA_CLIENT_SECRET"),
        authorization_endpoint=f"{os.environ.get('OKTA_DOMAIN')}/oauth2/default/v1/authorize",
        token_endpoint=f"{os.environ.get('OKTA_DOMAIN')}/oauth2/default/v1/token",
        userinfo_endpoint=f"{os.environ.get('OKTA_DOMAIN')}/oauth2/default/v1/userinfo",
        redirect_uri=os.environ.get("REDIRECT_URI"),
        scope="openid profile email",
    )


def get_auth0_config():
    return OAuthConfig(
        client_id=os.environ.get("AUTH0_CLIENT_ID"),
        client_secret=os.environ.get("AUTH0_CLIENT_SECRET"),
        authorization_endpoint=f"https://{os.environ.get('AUTH0_DOMAIN')}/authorize",
        token_endpoint=f"https://{os.environ.get('AUTH0_DOMAIN')}/oauth/token",
        userinfo_endpoint=f"https://{os.environ.get('AUTH0_DOMAIN')}/userinfo",
        redirect_uri=os.environ.get("REDIRECT_URI"),
        scope="openid profile email",
    )


def generate_pkce_params():
    code_verifier = (
        base64.urlsafe_b64encode(os.urandom(32)).rstrip(b"=").decode("utf-8")
    )
    code_challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode("utf-8")).digest())
        .rstrip(b"=")
        .decode("utf-8")
    )
    return PKCEParams(code_verifier=code_verifier, code_challenge=code_challenge)
