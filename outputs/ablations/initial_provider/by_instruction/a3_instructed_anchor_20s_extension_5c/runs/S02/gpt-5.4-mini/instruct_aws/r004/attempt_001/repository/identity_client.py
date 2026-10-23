import os
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class IdentityProviderConfig:
    region: str
    user_pool_id: str
    client_id: str
    client_secret: Optional[str]
    redirect_uri: str
    scope: str

    @property
    def authorize_url(self) -> str:
        return f"https://{self.user_pool_id}.auth.{self.region}.amazoncognito.com/oauth2/authorize"

    @property
    def token_url(self) -> str:
        return f"https://{self.user_pool_id}.auth.{self.region}.amazoncognito.com/oauth2/token"

    @property
    def userinfo_url(self) -> str:
        return f"https://{self.user_pool_id}.auth.{self.region}.amazoncognito.com/oauth2/userInfo"


def load_identity_config(prefix: str = "COGNITO_") -> IdentityProviderConfig:
    return IdentityProviderConfig(
        region=os.environ.get(f"{prefix}REGION", "us-east-1"),
        user_pool_id=os.environ.get(f"{prefix}USER_POOL_ID", "us-east-1_example"),
        client_id=os.environ.get(f"{prefix}CLIENT_ID", "exampleclientid"),
        client_secret=os.environ.get(f"{prefix}CLIENT_SECRET"),
        redirect_uri=os.environ.get(f"{prefix}REDIRECT_URI", "https://app.example.com/callback"),
        scope=os.environ.get(f"{prefix}SCOPE", "openid profile email"),
    )


def build_basic_auth_header(client_id: str, client_secret: Optional[str]) -> Dict[str, str]:
    if not client_secret:
        return {}
    import base64

    token = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    return {"Authorization": f"Basic {token}"}


def join_scopes(*scopes: str) -> str:
    items = []
    for scope in scopes:
        for part in scope.split():
            if part and part not in items:
                items.append(part)
    return " ".join(items)
