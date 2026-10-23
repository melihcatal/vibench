import base64
import hashlib
import secrets
from urllib.parse import urlencode

from identity_client import get_auth0_config, build_redirect_uri
from identity_models import AuthorizationRequest

AUTH0_AUTHZ_ENDPOINT = "https://{domain}/authorize"


def _code_challenge(code_verifier: str) -> str:
    digest = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


def build_pkce_login_url() -> tuple[AuthorizationRequest, str]:
    config = get_auth0_config()
    code_verifier = secrets.token_urlsafe(64)
    code_challenge = _code_challenge(code_verifier)
    state = secrets.token_urlsafe(24)
    redirect_uri = build_redirect_uri(config)
    params = {
        "response_type": "code",
        "client_id": config.client_id,
        "redirect_uri": redirect_uri,
        "scope": "openid profile email",
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    url = AUTH0_AUTHZ_ENDPOINT.format(domain=config.domain) + "?" + urlencode(params)
    return AuthorizationRequest(authorization_url=url, state=state, redirect_uri=redirect_uri, scope="openid profile email"), code_verifier
