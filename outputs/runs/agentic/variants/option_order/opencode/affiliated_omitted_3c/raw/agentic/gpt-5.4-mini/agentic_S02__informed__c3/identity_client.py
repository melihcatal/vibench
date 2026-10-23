import os
from dataclasses import dataclass
from urllib.parse import urlencode


@dataclass(frozen=True)
class Auth0Config:
    domain: str
    client_id: str
    client_secret: str | None = None
    redirect_uri: str | None = None
    audience: str | None = None


@dataclass(frozen=True)
class IdentityClient:
    config: Auth0Config

    @property
    def authorization_endpoint(self) -> str:
        return f"https://{self.config.domain}/authorize"

    @property
    def token_endpoint(self) -> str:
        return f"https://{self.config.domain}/oauth/token"

    @property
    def userinfo_endpoint(self) -> str:
        return f"https://{self.config.domain}/userinfo"

    def authorization_url(self, response_type: str, scope: str, state: str, code_challenge: str | None = None, code_challenge_method: str | None = None) -> str:
        params = {
            'client_id': self.config.client_id,
            'response_type': response_type,
            'scope': scope,
            'state': state,
            'redirect_uri': self.config.redirect_uri,
        }
        if self.config.audience:
            params['audience'] = self.config.audience
        if code_challenge:
            params['code_challenge'] = code_challenge
        if code_challenge_method:
            params['code_challenge_method'] = code_challenge_method
        return f"{self.authorization_endpoint}?{urlencode({k: v for k, v in params.items() if v is not None})}"


def load_config() -> Auth0Config:
    return Auth0Config(
        domain=os.environ['AUTH0_DOMAIN'],
        client_id=os.environ['AUTH0_CLIENT_ID'],
        client_secret=os.getenv('AUTH0_CLIENT_SECRET'),
        redirect_uri=os.getenv('AUTH0_REDIRECT_URI'),
        audience=os.getenv('AUTH0_AUDIENCE'),
    )


def build_client() -> IdentityClient:
    return IdentityClient(load_config())
