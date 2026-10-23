import os
from dataclasses import dataclass
from typing import Dict, Optional

import requests


@dataclass(frozen=True)
class FederatedLoginConfig:
    issuer_url: str
    client_id: str
    client_secret: Optional[str]
    redirect_uri: str
    scopes: str


def load_federated_login_config() -> FederatedLoginConfig:
    issuer_url = os.environ.get("OKTA_ISSUER_URL") or os.environ.get("AUTH_ISSUER_URL")
    client_id = os.environ.get("OKTA_CLIENT_ID") or os.environ.get("AUTH_CLIENT_ID")
    client_secret = os.environ.get("OKTA_CLIENT_SECRET") or os.environ.get("AUTH_CLIENT_SECRET")
    redirect_uri = os.environ.get("OKTA_REDIRECT_URI") or os.environ.get("AUTH_REDIRECT_URI")
    scopes = os.environ.get("OKTA_SCOPES") or os.environ.get("AUTH_SCOPES") or "openid profile email"

    if not issuer_url:
        raise ValueError("Missing issuer URL: set OKTA_ISSUER_URL or AUTH_ISSUER_URL")
    if not client_id:
        raise ValueError("Missing client ID: set OKTA_CLIENT_ID or AUTH_CLIENT_ID")
    if not redirect_uri:
        raise ValueError("Missing redirect URI: set OKTA_REDIRECT_URI or AUTH_REDIRECT_URI")

    return FederatedLoginConfig(
        issuer_url=issuer_url.rstrip("/"),
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scopes=scopes,
    )


class FederatedLoginClient:
    def __init__(self, config: Optional[FederatedLoginConfig] = None):
        self.config = config or load_federated_login_config()

    def authorization_url(self, state: str, nonce: Optional[str] = None, prompt: Optional[str] = None) -> str:
        params: Dict[str, str] = {
            "client_id": self.config.client_id,
            "response_type": "code",
            "scope": self.config.scopes,
            "redirect_uri": self.config.redirect_uri,
            "state": state,
        }
        if nonce:
            params["nonce"] = nonce
        if prompt:
            params["prompt"] = prompt
        return f"{self.config.issuer_url}/v1/authorize?" + requests.compat.urlencode(params)

    def exchange_code_for_tokens(self, code: str) -> Dict[str, object]:
        token_url = f"{self.config.issuer_url}/v1/token"
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.config.redirect_uri,
        }
        auth = None
        if self.config.client_secret:
            auth = (self.config.client_id, self.config.client_secret)
        else:
            data["client_id"] = self.config.client_id
        response = requests.post(token_url, data=data, auth=auth, timeout=30)
        response.raise_for_status()
        return response.json()

    def fetch_userinfo(self, access_token: str) -> Dict[str, object]:
        userinfo_url = f"{self.config.issuer_url}/v1/userinfo"
        response = requests.get(
            userinfo_url,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()
